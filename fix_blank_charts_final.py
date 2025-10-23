#!/usr/bin/env python3
"""
Final fix: Add ctx definition exactly where it should be, matching exemplar structure.
"""

import re
from pathlib import Path

def fix_blank_charts(file_path):
    """Add ctx and DPI fix in exact exemplar structure."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find: const canvas = document.getElementById('severityChart');
    # followed by blank lines, and replace with the correct structure

    # Pattern to find the canvas line followed by whitespace
    pattern = r"(// Create chart with custom plugin for colored squares\s*const canvas = document\.getElementById\('severityChart'\);)\s*\n\s*\n\s*\n\s*(let hoveredExpertIndex)"

    # Replacement with ctx definition
    replacement = r'''\1
        const ctx = document.getElementById('severityChart').getContext('2d');

        \2'''

    content = re.sub(pattern, replacement, content)

    # Now add the DPI fix after medianValuesPlugin closes
    # Find the closing of medianValuesPlugin
    dpi_fix = '''
        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const canvas = document.getElementById('severityChart');
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
'''

    # Pattern: end of medianValuesPlugin, before any // Track hover or chartCanvas references
    # Look for the plugin closing followed by whitespace
    plugin_pattern = r'(const medianValuesPlugin = \{[^}]*afterDatasetsDraw: \(chart\) => \{(?:[^{}]|\{[^{}]*\})*\}\s*\};)\s*\n(\s*const chartCanvas|// Track|let hoveredExpertIndex)'

    # Check if DPI fix is already there
    if '// Fix blurry canvas on high-DPI displays' not in content:
        # Insert after the plugin
        plugin_replacement = r'\1' + dpi_fix + '\n\2'
        content = re.sub(plugin_pattern, plugin_replacement, content, flags=re.DOTALL)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated: {file_path.name}")


def main():
    """Process all severity chart files."""

    # Find all BAU and PM severity charts
    bau_charts = sorted(Path('.').glob('risk*_bau_chart.html'))
    pm_charts = sorted(Path('.').glob('risk*_pm_chart.html'))

    all_charts = bau_charts + pm_charts

    if not all_charts:
        print("No severity charts found!")
        return

    print(f"Found {len(all_charts)} severity charts")
    print(f"Adding ctx definition and DPI fix...\n")

    for chart_file in all_charts:
        fix_blank_charts(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

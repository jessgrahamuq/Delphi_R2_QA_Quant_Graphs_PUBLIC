#!/usr/bin/env python3
"""
Add only the DPI fix after medianValuesPlugin.
"""

import re
from pathlib import Path

def add_dpi_fix(file_path):
    """Add DPI fix after medianValuesPlugin closes."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has DPI fix
    if '// Fix blurry canvas on high-DPI displays' in content:
        print(f"Skipped (already has DPI fix): {file_path.name}")
        return

    dpi_fix = '''
        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const canvas = document.getElementById('severityChart');
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
'''

    # Find the closing of medianValuesPlugin and add DPI fix after it
    # Pattern: the closing }; of the plugin
    pattern = r'(const medianValuesPlugin = \{[^}]*id: ["\']medianValues["\'][^}]*afterDatasetsDraw:[^}]*\}(?:[^}]*\{[^}]*\}[^}]*)*\s*\};)'

    def replace_func(match):
        return match.group(1) + dpi_fix

    content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

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
    print(f"Adding DPI fix after medianValuesPlugin...\n")

    for chart_file in all_charts:
        add_dpi_fix(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

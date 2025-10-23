#!/usr/bin/env python3
"""
Properly fix the missing ctx by inserting after canvas definition.
"""

import re
from pathlib import Path

def fix_ctx_properly(file_path):
    """Insert ctx and DPI fix right after canvas is defined."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # DPI fix code to insert
    dpi_fix = """
        // Fix blurry canvas on high-DPI displays
        const ctx = document.getElementById('severityChart').getContext('2d');
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
"""

    # Find the canvas definition and insert DPI fix right after it
    # Look for: const canvas = document.getElementById('severityChart');
    # followed by blank lines and then // Track hover state

    pattern = r"(const canvas = document\.getElementById\('severityChart'\);)\s*\n\s*\n\s*(/\/ Track hover state)"

    replacement = r"\1" + dpi_fix + "\n        \2"

    content = re.sub(pattern, replacement, content)

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
    print(f"Properly inserting ctx and DPI fix...\n")

    for chart_file in all_charts:
        fix_ctx_properly(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

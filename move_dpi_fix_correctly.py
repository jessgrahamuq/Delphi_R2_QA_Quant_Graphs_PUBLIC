#!/usr/bin/env python3
"""
Move DPI fix to the correct location - right before chart creation.
"""

from pathlib import Path
import re

def move_dpi_fix(file_path):
    """Move DPI fix to right before chart creation."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # First, remove the existing DPI fix wherever it is
    dpi_fix_pattern = r'\n        // Fix blurry canvas on high-DPI displays\n        const dpr = window\.devicePixelRatio \|\| 1;\n        const rect = canvas\.getBoundingClientRect\(\);\n        canvas\.width = rect\.width \* dpr;\n        canvas\.height = rect\.height \* dpr;\n        ctx\.scale\(dpr, dpr\);\n'

    content = re.sub(dpi_fix_pattern, '', content)

    # Now add it right before "const chart = new Chart"
    dpi_fix = '''        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);

'''

    # Find "const chart = new Chart" and add DPI fix before it
    chart_pattern = r'(        const chart = new Chart\(ctx,)'
    replacement = dpi_fix + r'\1'

    if re.search(chart_pattern, content):
        content = re.sub(chart_pattern, replacement, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Fixed: {file_path.name}")
    else:
        print(f"ERROR: Could not find chart creation in {file_path.name}")


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
    print(f"Moving DPI fix to correct location...\n")

    for chart_file in all_charts:
        move_dpi_fix(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

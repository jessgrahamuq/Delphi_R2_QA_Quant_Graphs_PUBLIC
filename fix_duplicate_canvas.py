#!/usr/bin/env python3
"""
Fix duplicate canvas declaration in DPI fix.
Change 'const canvas' to just use the existing canvas variable.
"""

from pathlib import Path

def fix_duplicate_canvas(file_path):
    """Fix duplicate canvas declaration."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the duplicate canvas declaration in DPI fix
    old_dpi_fix = '''        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const canvas = document.getElementById('severityChart');
        const rect = canvas.getBoundingClientRect();'''

    new_dpi_fix = '''        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();'''

    if old_dpi_fix in content:
        content = content.replace(old_dpi_fix, new_dpi_fix)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Fixed: {file_path.name}")
    else:
        print(f"Skipped (pattern not found): {file_path.name}")


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
    print(f"Fixing duplicate canvas declarations...\n")

    for chart_file in all_charts:
        fix_duplicate_canvas(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

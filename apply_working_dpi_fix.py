#!/usr/bin/env python3
"""
Apply the working DPI fix from exemplar chart to all severity charts.
"""

import re
from pathlib import Path

def apply_dpi_fix(file_path):
    """Apply the exact DPI fix that works in exemplar chart."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any existing DPI fix code
    content = re.sub(
        r'// Fix blurry canvas on high-DPI displays.*?ctx\.scale\(dpr, dpr\);',
        '',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'// Set up high-DPI canvas.*?ctx\.scale\(dpr, dpr\);',
        '',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'// Handle iframe resize.*?setTimeout\(handleResize, 500\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Find where ctx is defined and replace it with the working solution
    # Pattern: const ctx = something.getContext('2d');

    working_fix = '''const ctx = document.getElementById('severityChart').getContext('2d');

        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const canvas = document.getElementById('severityChart');
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);'''

    # Replace the ctx definition
    content = re.sub(
        r'const canvas = document\.getElementById\(\'severityChart\'\);.*?const ctx = canvas\.getContext\(\'2d\'\);',
        working_fix,
        content,
        flags=re.DOTALL
    )

    # Also handle simpler case
    content = re.sub(
        r'const ctx = document\.getElementById\(\'severityChart\'\)\.getContext\(\'2d\'\);',
        working_fix,
        content
    )

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated: {file_path.name}")


def main():
    """Process all severity chart files."""

    # Find all BAU and PM severity charts (not the exemplar)
    bau_charts = sorted(Path('.').glob('risk*_bau_chart.html'))
    pm_charts = sorted(Path('.').glob('risk*_pm_chart.html'))

    all_charts = bau_charts + pm_charts

    if not all_charts:
        print("No severity charts found!")
        return

    print(f"Found {len(all_charts)} severity charts")
    print(f"Applying working DPI fix from exemplar chart...\n")

    for chart_file in all_charts:
        apply_dpi_fix(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

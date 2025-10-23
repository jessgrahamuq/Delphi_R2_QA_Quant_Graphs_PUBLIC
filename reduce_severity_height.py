#!/usr/bin/env python3
"""
Script to reduce the height of severity charts.
"""

import re
from pathlib import Path

def reduce_chart_height(file_path, new_height=350):
    """Reduce the chart height in a severity chart file and change background to white."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the height in .chart-container
    # Looking for: height: 500px;
    content = re.sub(
        r'(\.chart-container\s*\{[^}]*height:\s*)\d+px;',
        rf'\g<1>{new_height}px;',
        content
    )

    # Change body background from grey to white
    # Looking for: background: #f5f5f5;
    content = re.sub(
        r'(body\s*\{[^}]*background:\s*)#f5f5f5;',
        r'\g<1>white;',
        content
    )

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
    print(f"Reducing height to 350px and changing background to white...\n")

    for chart_file in all_charts:
        reduce_chart_height(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

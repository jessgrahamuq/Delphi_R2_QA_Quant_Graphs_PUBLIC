#!/usr/bin/env python3
"""
Script to reduce title text size and chart height in severity charts.
"""

import re
from pathlib import Path

def reduce_sizes(file_path):
    """Reduce title text size and chart height."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reduce banner font size (the title with risk name)
    content = re.sub(
        r'(\.banner\s*\{[^}]*font-size:\s*)\d+px;',
        r'\g<1>14px;',
        content
    )

    # Reduce banner padding for more compact appearance
    content = re.sub(
        r'(\.banner\s*\{[^}]*padding:\s*)10px 20px;',
        r'\g<1>8px 15px;',
        content
    )

    # Reduce chart height further (from 350px to 280px)
    content = re.sub(
        r'(\.chart-container\s*\{[^}]*height:\s*)\d+px;',
        r'\g<1>280px;',
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
    print(f"Reducing title size and chart height...\n")

    for chart_file in all_charts:
        reduce_sizes(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

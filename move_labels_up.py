#!/usr/bin/env python3
"""
Script to move harm labels up to use white space and prevent overlap with legend.
"""

import re
from pathlib import Path

def move_labels_up(file_path):
    """Move severity labels up to use available white space."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change the severity-labels margin-top to move them up significantly
    content = re.sub(
        r'(\.severity-labels\s*\{[^}]*margin-top:\s*)-?\d+px;',
        r'\g<1>-15px;',
        content
    )

    # Also reduce bottom margin to create more space
    content = re.sub(
        r'(\.severity-labels\s*\{[^}]*margin-bottom:\s*)\d+px;',
        r'\g<1>5px;',
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
    print(f"Moving harm labels up...\n")

    for chart_file in all_charts:
        move_labels_up(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

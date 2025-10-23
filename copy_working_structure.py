#!/usr/bin/env python3
"""
Copy the working structure from risk1_bau_chart_updated.html to all other severity charts.
"""

from pathlib import Path
import re

def copy_structure(source_file, target_file):
    """Copy the script structure from source to target."""

    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    with open(target_file, 'r', encoding='utf-8') as f:
        target_content = f.read()

    # Extract the key parts from source:
    # 1. The section from "const ctx = " to just before "const chart = new Chart"
    source_pattern = r'(        const ctx = document\.getElementById.*?)(        const chart = new Chart\(ctx,)'
    source_match = re.search(source_pattern, source_content, re.DOTALL)

    if not source_match:
        print(f"ERROR: Could not find pattern in source file")
        return False

    source_structure = source_match.group(1)

    # Replace the same section in target
    target_pattern = r'(        const ctx = document\.getElementById.*?)(        const chart = new Chart\(ctx,)'

    if not re.search(target_pattern, target_content, re.DOTALL):
        print(f"ERROR: Could not find pattern in {target_file.name}")
        return False

    new_content = re.sub(target_pattern, source_structure + r'\2', target_content, flags=re.DOTALL)

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    """Process all severity chart files."""

    source = Path('risk1_bau_chart_updated.html')
    if not source.exists():
        print("ERROR: Source file risk1_bau_chart_updated.html not found!")
        return

    # Find all BAU and PM severity charts (exclude the source file and the updated file)
    bau_charts = [f for f in Path('.').glob('risk*_bau_chart.html') if f.name != 'risk1_bau_chart_updated.html']
    pm_charts = list(Path('.').glob('risk*_pm_chart.html'))

    all_charts = sorted(bau_charts + pm_charts)

    if not all_charts:
        print("No severity charts found!")
        return

    print(f"Found {len(all_charts)} severity charts to update")
    print(f"Copying structure from {source.name}...\n")

    success_count = 0
    for chart_file in all_charts:
        if copy_structure(source, chart_file):
            print(f"Updated: {chart_file.name}")
            success_count += 1
        else:
            print(f"FAILED: {chart_file.name}")

    print(f"\nCompleted! Successfully updated {success_count}/{len(all_charts)} files")


if __name__ == '__main__':
    main()

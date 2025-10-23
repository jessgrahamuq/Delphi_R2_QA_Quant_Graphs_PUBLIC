#!/usr/bin/env python3
"""
Script to split sector vulnerability charts into 4 groups.
14 sectors total: 4 groups with 4, 4, 4, and 2 sectors respectively.
"""

import os
import re
from pathlib import Path

# Define sector groups (4, 4, 4, 2)
SECTOR_GROUPS = {
    1: [
        "Agriculture",
        "Trade",
        "Information",
        "Finance"
    ],
    2: [
        "Real_Estate",
        "Professional",
        "Scientific",
        "Management"
    ],
    3: [
        "Education",
        "Health_Care",
        "Arts",
        "Accommodation"
    ],
    4: [
        "Public_Admin",
        "National_Security"
    ]
}

def split_sector_chart(input_file, output_dir):
    """Split a sector chart into 4 group charts."""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the risk title from the file
    title_match = re.search(r'<title>(.*?)</title>', content)
    original_title = title_match.group(1) if title_match else ""

    # Split into lines
    lines = content.split('\n')

    # Find where tbody starts and ends
    tbody_start = None
    tbody_end = None
    for i, line in enumerate(lines):
        if '<tbody>' in line:
            tbody_start = i
        if '</tbody>' in line:
            tbody_end = i
            break

    if tbody_start is None or tbody_end is None:
        print(f"Could not find tbody in {input_file}")
        return []

    # Extract sector rows
    sector_rows = {}
    current_sector = None
    current_row_lines = []

    for i in range(tbody_start + 1, tbody_end):
        line = lines[i]

        # Check if this is the start of a new sector row
        sector_match = re.search(r'data-sector="([^"]+)"', line)
        if sector_match:
            # Save previous sector if exists
            if current_sector and current_row_lines:
                sector_rows[current_sector] = current_row_lines

            # Start new sector
            current_sector = sector_match.group(1)
            current_row_lines = [line]
        else:
            if current_sector:
                current_row_lines.append(line)

    # Save last sector
    if current_sector and current_row_lines:
        sector_rows[current_sector] = current_row_lines

    # Extract risk number from input filename
    risk_match = re.search(r'risk_(\d+)_sector_vulnerability\.html', input_file.name)
    if not risk_match:
        print(f"Could not extract risk number from {input_file.name}")
        return []

    risk_num = risk_match.group(1)

    created_files = []

    # Create charts for each group
    for group_num, sectors in SECTOR_GROUPS.items():
        # Collect rows for this group
        group_rows = []
        for sector in sectors:
            if sector in sector_rows:
                group_rows.extend(sector_rows[sector])

        if not group_rows:
            print(f"Warning: No sectors found for group {group_num} in risk {risk_num}")
            continue

        # Build group chart
        group_content = lines[:tbody_start + 1] + group_rows + lines[tbody_end:]
        group_content = '\n'.join(group_content)

        # Update title
        group_content = group_content.replace(
            original_title,
            original_title.replace('All Sectors', f'Sectors Group {group_num}')
        )

        # Write output file
        output_file = output_dir / f'risk_{risk_num}_sector_vulnerability_group{group_num}.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(group_content)

        created_files.append(output_file)
        print(f"Created: {output_file}")

    return created_files


def main():
    """Process all sector vulnerability chart files."""
    sec_dir = Path('Sec_Charts')

    # Find all existing sector chart files
    chart_files = sorted(sec_dir.glob('risk_*_sector_vulnerability.html'))

    all_created = []
    for chart_file in chart_files:
        print(f"\nProcessing {chart_file.name}...")
        created = split_sector_chart(chart_file, sec_dir)
        all_created.extend(created)

    print(f"\n\nTotal files created: {len(all_created)}")


if __name__ == '__main__':
    main()

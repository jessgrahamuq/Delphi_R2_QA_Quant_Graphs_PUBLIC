#!/usr/bin/env python3
"""
Script to split responsibility actor charts into required and optional actors.
"""

import os
import re
from pathlib import Path

# Define actor categories (same as vulnerability charts)
REQUIRED_ACTORS = [
    "ai_dev_gen",      # AI Developer (General-purpose AI)
    "ai_deployer",     # AI Deployer
    "ai_gov_actor",    # AI Governance Actor
    "ai_user"          # AI User
]

OPTIONAL_ACTORS = [
    "ai_dev_spec",     # AI Developer (Specialized AI)
    "ai_infra",        # AI Infrastructure Provider
    "ai_stake"         # Affected Stakeholder
]

def split_chart(input_file, output_required, output_optional):
    """Split a responsibility chart into required and optional actor charts."""

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
        return

    # Extract actor rows
    actor_rows = {}
    current_actor = None
    current_row_lines = []

    for i in range(tbody_start + 1, tbody_end):
        line = lines[i]

        # Check if this is the start of a new actor row
        actor_match = re.search(r'data-actor="([^"]+)"', line)
        if actor_match:
            # Save previous actor if exists
            if current_actor and current_row_lines:
                actor_rows[current_actor] = current_row_lines

            # Start new actor
            current_actor = actor_match.group(1)
            current_row_lines = [line]
        else:
            if current_actor:
                current_row_lines.append(line)

    # Save last actor
    if current_actor and current_row_lines:
        actor_rows[current_actor] = current_row_lines

    # Create required actors chart
    required_rows = []
    for actor in REQUIRED_ACTORS:
        if actor in actor_rows:
            required_rows.extend(actor_rows[actor])

    # Create optional actors chart
    optional_rows = []
    for actor in OPTIONAL_ACTORS:
        if actor in actor_rows:
            optional_rows.extend(actor_rows[actor])

    # Build required chart
    required_content = lines[:tbody_start + 1] + required_rows + lines[tbody_end:]
    required_content = '\n'.join(required_content)
    required_content = required_content.replace(
        original_title,
        original_title.replace('All Actors', 'Required Actors')
    )

    # Build optional chart
    optional_content = lines[:tbody_start + 1] + optional_rows + lines[tbody_end:]
    optional_content = '\n'.join(optional_content)
    optional_content = optional_content.replace(
        original_title,
        original_title.replace('All Actors', 'Optional Actors')
    )

    # Write output files
    with open(output_required, 'w', encoding='utf-8') as f:
        f.write(required_content)

    with open(output_optional, 'w', encoding='utf-8') as f:
        f.write(optional_content)

    print(f"Created: {output_required}")
    print(f"Created: {output_optional}")


def main():
    """Process all responsibility chart files."""
    resp_dir = Path('Resp_Charts')

    # Find all existing resp chart files
    chart_files = sorted(resp_dir.glob('risk*_resp_actors_chart.html'))

    for chart_file in chart_files:
        # Extract risk number
        risk_match = re.search(r'risk(\d+)_resp_actors_chart\.html', chart_file.name)
        if not risk_match:
            continue

        risk_num = risk_match.group(1)

        # Create output file paths
        output_required = resp_dir / f'risk{risk_num}_resp_actors_required_chart.html'
        output_optional = resp_dir / f'risk{risk_num}_resp_actors_optional_chart.html'

        print(f"\nProcessing {chart_file.name}...")
        split_chart(chart_file, output_required, output_optional)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Apply the working JavaScript structure from risk1_bau_chart_updated.html to all charts.
Keep each chart's unique data but use the working code structure.
"""

from pathlib import Path
import re

def extract_data(content):
    """Extract the unique data arrays from a chart file."""

    # Extract expert data
    expert_data_match = re.search(r'const expertData = (\[.*?\]);', content, re.DOTALL)
    expert_data = expert_data_match.group(1) if expert_data_match else None

    # Extract exceedance data
    exceedance_match = re.search(r'const exceedanceData = (\[.*?\]);', content, re.DOTALL)
    exceedance_data = exceedance_match.group(1) if exceedance_match else None

    # Extract risk info
    risk_match = re.search(r'<div class="banner">\s*([\d.]+\s+.*?)</div>', content, re.DOTALL)
    risk_info = risk_match.group(1).strip() if risk_match else None

    return {
        'expert_data': expert_data,
        'exceedance_data': exceedance_data,
        'risk_info': risk_info
    }


def apply_template(template_content, data):
    """Apply template with unique data."""

    result = template_content

    # Replace expert data
    if data['expert_data']:
        result = re.sub(
            r'const expertData = \[.*?\];',
            f'const expertData = {data["expert_data"]};',
            result,
            flags=re.DOTALL
        )

    # Replace exceedance data
    if data['exceedance_data']:
        result = re.sub(
            r'const exceedanceData = \[.*?\];',
            f'const exceedanceData = {data["exceedance_data"]};',
            result,
            flags=re.DOTALL
        )

    # Replace risk info
    if data['risk_info']:
        result = re.sub(
            r'<div class="banner">[\d.]+\s+.*?</div>',
            f'<div class="banner">{data["risk_info"]}</div>',
            result,
            flags=re.DOTALL
        )

    return result


def main():
    """Process all severity chart files."""

    template_file = Path('risk1_bau_chart_updated.html')
    if not template_file.exists():
        print("ERROR: Template file risk1_bau_chart_updated.html not found!")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Find all charts except the template
    all_charts = []
    for pattern in ['risk*_bau_chart.html', 'risk*_pm_chart.html']:
        all_charts.extend([f for f in Path('.').glob(pattern) if f.name != 'risk1_bau_chart_updated.html'])

    all_charts = sorted(set(all_charts))

    if not all_charts:
        print("No charts found!")
        return

    print(f"Found {len(all_charts)} charts to update")
    print(f"Using template: {template_file.name}\n")

    for chart_file in all_charts:
        with open(chart_file, 'r', encoding='utf-8') as f:
            chart_content = f.read()

        # Extract unique data from this chart
        data = extract_data(chart_content)

        # Apply template with this chart's data
        new_content = apply_template(template_content, data)

        # Write back
        with open(chart_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Updated: {chart_file.name}")

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

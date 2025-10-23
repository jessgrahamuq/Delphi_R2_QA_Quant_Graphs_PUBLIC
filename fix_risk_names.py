#!/usr/bin/env python3
"""
Fix risk names in banner to match the filename.
"""

from pathlib import Path
import re

# Mapping of risk numbers to names (you'll need to provide the actual names)
RISK_NAMES = {
    1: "1.1 Unfair discrimination and misrepresentation",
    2: "1.2 Erosion of privacy",
    3: "2.1 Underuse or non-use of AI due to misplaced fears",
    4: "2.2 Unauthorized and harmful uses",
    5: "3.1 Overreliance and unsafe use",
    6: "3.2 Goal misspecification or gaming",
    7: "3.3 Hazardous task execution",
    8: "4.1 Harmful content generation",
    9: "4.2 Malicious use",
    10: "5.1 Value misalignment",
    11: "5.2 Persuasive and manipulative capabilities",
    12: "6.1 AI-enabled cyberattacks",
    13: "6.2 Accidents and structural failures",
    14: "6.3 Poor product design",
    15: "7.1 Intellectual property violations",
    16: "7.2 Unaccountable AI-caused harms",
    17: "7.3 Unfair market dynamics",
    18: "8.1 Negative impacts on labor markets",
    19: "8.2 Geopolitical instability",
    20: "8.3 Societal fragmentation and polarization",
    21: "9.1 Model theft",
    22: "9.2 Data poisoning and other tampering",
    23: "10.1 Autonomous decision-making",
    24: "10.2 Loss of control and autonomous replication"
}

def fix_risk_name(file_path):
    """Fix the risk name in the banner."""

    # Extract risk number and scenario from filename
    match = re.match(r'risk(\d+)_(bau|pm)_chart\.html', file_path.name)
    if not match:
        print(f"ERROR: Could not parse filename {file_path.name}")
        return

    risk_num = int(match.group(1))
    scenario = "Business as usual" if match.group(2) == "bau" else "Pragmatic mitigations"

    if risk_num not in RISK_NAMES:
        print(f"ERROR: No name found for risk {risk_num}")
        return

    risk_name = RISK_NAMES[risk_num]
    new_banner_text = f"{risk_name} / {scenario}"

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace banner text
    content = re.sub(
        r'<div class="banner">\s*[\d.]+\s+[^/]+/[^<]+</div>',
        f'<div class="banner">\n            {new_banner_text}\n        </div>',
        content
    )

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated: {file_path.name} -> {new_banner_text}")


def main():
    """Process all severity chart files."""

    # Find all BAU and PM severity charts
    all_charts = sorted(Path('.').glob('risk*_bau_chart.html')) + \
                 sorted(Path('.').glob('risk*_pm_chart.html'))

    if not all_charts:
        print("No severity charts found!")
        return

    print(f"Found {len(all_charts)} severity charts")
    print(f"Fixing risk names...\n")

    for chart_file in all_charts:
        fix_risk_name(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

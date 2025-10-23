#!/usr/bin/env python3
"""
Fix risk names in banner to match the filename.
"""

from pathlib import Path
import re

# Mapping of risk numbers to names from index.html
RISK_NAMES = {
    1: "1.1 Unfair discrimination and misrepresentation",
    2: "1.2 Exposure to toxic content",
    3: "1.3 Unequal performance across groups",
    4: "2.1 Compromise of privacy by obtaining, leaking or correctly inferring sensitive information",
    5: "2.2 AI system security vulnerabilities and attacks",
    6: "3.2 False or misleading information",
    7: "3.1 Pollution of information ecosystem and loss of consensus reality",
    8: "4.1 Disinformation, surveillance, and influence at scale",
    9: "4.3 Cyberattacks, weapon development or use, and mass harm",
    10: "4.2 Fraud, scams, and targeted manipulation",
    11: "5.1 Overreliance and unsafe use",
    12: "5.2 Loss of human agency and autonomy",
    13: "6.1 Power centralization and unfair distribution of benefits",
    14: "6.2 Increased inequality and decline in employment quality",
    15: "6.3 Economic and cultural devaluation of human effort",
    16: "6.4 Competitive dynamics",
    17: "6.5 Governance failure",
    18: "6.6 Environmental harm",
    19: "7.1 AI pursuing its own goals in conflict with human goals or values",
    20: "7.2 AI possessing dangerous capabilities",
    21: "7.3 Lack of capability or robustness",
    22: "7.4 Lack of transparency or interpretability",
    23: "7.5 AI welfare and rights",
    24: "7.6 Multi-agent risks"
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

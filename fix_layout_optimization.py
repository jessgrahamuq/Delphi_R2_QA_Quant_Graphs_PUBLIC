#!/usr/bin/env python3
"""
Script to fix label positioning, optimize white space, and make legends more compact.
"""

import re
from pathlib import Path

def fix_layout(file_path):
    """Optimize the layout with better label positioning and compact legends."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix severity labels positioning - align them better with chart columns
    # Remove the previous positioning and replace with better values
    severity_label_positions = r'''        .severity-label:nth-child(1) { left: 10%; transform: translateX(-50%); }
        .severity-label:nth-child(2) { left: 30%; transform: translateX(-50%); }
        .severity-label:nth-child(3) { left: 50%; transform: translateX(-50%); }
        .severity-label:nth-child(4) { left: 70%; transform: translateX(-50%); }
        .severity-label:nth-child(5) { left: 90%; transform: translateX(-50%); }'''

    # Replace all severity-label:nth-child positioning
    content = re.sub(
        r'\.severity-label:nth-child\(1\)[^}]*\}',
        '',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(2\)[^}]*\}',
        '',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(3\)[^}]*\}',
        '',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(4\)[^}]*\}',
        '',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(5\)[^}]*\}',
        '',
        content
    )

    # Add the new positioning before the media query
    media_query_pos = content.find('@media (max-width: 600px)')
    if media_query_pos != -1:
        content = content[:media_query_pos] + severity_label_positions + '\n        ' + content[media_query_pos:]

    # Update severity-label CSS to reduce max-width and adjust size
    severity_label_css = r'''        .severity-label {
            font-size: 13px;
            font-weight: bold;
            white-space: normal;
            position: absolute;
            max-width: 16%;
            text-align: center;
            line-height: 1.1;
            word-wrap: break-word;
            hyphens: auto;
        }'''

    content = re.sub(
        r'\.severity-label\s*\{[^}]*\}',
        severity_label_css,
        content,
        flags=re.DOTALL
    )

    # Make the legend more compact
    legend_css = r'''        .legend {
            margin-top: 15px;
            padding: 8px 10px;
            background: #f9f9f9;
            border-radius: 4px;
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }'''

    content = re.sub(
        r'\.legend\s*\{[^}]*\}',
        legend_css,
        content,
        flags=re.DOTALL
    )

    # Make legend items more compact
    legend_item_css = r'''        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            font-weight: 500;
        }'''

    content = re.sub(
        r'\.legend-item\s*\{[^}]*\}',
        legend_item_css,
        content,
        flags=re.DOTALL
    )

    # Reduce severity-labels margin
    content = re.sub(
        r'(\.severity-labels\s*\{[^}]*margin-top:\s*)-?\d+px;',
        r'\g<1>-5px;',
        content
    )
    content = re.sub(
        r'(\.severity-labels\s*\{[^}]*margin-bottom:\s*)\d+px;',
        r'\g<1>8px;',
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
    print(f"Optimizing layout and positioning...\n")

    for chart_file in all_charts:
        fix_layout(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Revert harm labels to original positioning and wrapping.
"""

import re
from pathlib import Path

def revert_labels(file_path):
    """Revert severity labels to original state."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Original severity-label CSS (no wrapping, larger font)
    original_label_css = r'''        .severity-label {
            font-size: 17px;
            font-weight: bold;
            white-space: nowrap;
            position: absolute;
        }'''

    content = re.sub(
        r'\.severity-label\s*\{[^}]*\}',
        original_label_css,
        content,
        flags=re.DOTALL
    )

    # Remove all nth-child positioning
    content = re.sub(
        r'\.severity-label:nth-child\(\d+\)[^}]*\}',
        '',
        content
    )

    # Add back original positioning
    original_positions = '''        .severity-label:nth-child(1) { left: 8%; transform: translateX(0%); }
        .severity-label:nth-child(2) { left: 32%; transform: translateX(-50%); }
        .severity-label:nth-child(3) { left: 52%; transform: translateX(-50%); }
        .severity-label:nth-child(4) { left: 70%; transform: translateX(-50%); }
        .severity-label:nth-child(5) { left: 95%; transform: translateX(-100%); }'''

    # Find the severity-label closing brace and add positioning after it
    # Insert before media query or before style closing
    media_query_pos = content.find('@media (max-width: 600px)')
    if media_query_pos != -1:
        content = content[:media_query_pos] + original_positions + '\n        ' + content[media_query_pos:]
    else:
        # Insert before </style>
        style_close = content.find('</style>')
        if style_close != -1:
            content = content[:style_close] + original_positions + '\n' + content[style_close:]

    # Remove the media query for labels if it exists
    content = re.sub(
        r'@media \(max-width: 600px\)\s*\{[^}]*\.severity-label[^}]*\}[^}]*\}',
        '',
        content
    )

    # Restore original severity-labels container margins
    content = re.sub(
        r'(\.severity-labels\s*\{[^}]*margin-top:\s*)-?\d+px;',
        r'\g<1>-10px;',
        content
    )
    content = re.sub(
        r'(\.severity-labels\s*\{[^}]*margin-bottom:\s*)\d+px;',
        r'\g<1>10px;',
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
    print(f"Reverting harm labels to original positioning...\n")

    for chart_file in all_charts:
        revert_labels(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

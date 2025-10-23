#!/usr/bin/env python3
"""
Script to fix canvas resolution for sharp rendering and wrap severity labels.
"""

import re
from pathlib import Path

def fix_rendering_and_labels(file_path):
    """Fix canvas rendering and make labels wrap at narrow widths."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix severity label CSS to allow wrapping and prevent overlap
    severity_label_css = r'''        .severity-label {
            font-size: 14px;
            font-weight: bold;
            white-space: normal;
            position: absolute;
            max-width: 18%;
            text-align: center;
            line-height: 1.2;
            word-wrap: break-word;
            hyphens: auto;
        }'''

    content = re.sub(
        r'\.severity-label\s*\{[^}]*\}',
        severity_label_css,
        content,
        flags=re.DOTALL
    )

    # Adjust positioning to prevent overlap at narrow widths
    content = re.sub(
        r'\.severity-label:nth-child\(1\)[^}]*\}',
        r'.severity-label:nth-child(1) { left: 9%; transform: translateX(-50%); }',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(2\)[^}]*\}',
        r'.severity-label:nth-child(2) { left: 28%; transform: translateX(-50%); }',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(3\)[^}]*\}',
        r'.severity-label:nth-child(3) { left: 50%; transform: translateX(-50%); }',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(4\)[^}]*\}',
        r'.severity-label:nth-child(4) { left: 72%; transform: translateX(-50%); }',
        content
    )
    content = re.sub(
        r'\.severity-label:nth-child\(5\)[^}]*\}',
        r'.severity-label:nth-child(5) { left: 91%; transform: translateX(-50%); }',
        content
    )

    # Add media query for responsive font sizing
    media_query = '''
        @media (max-width: 600px) {
            .severity-label {
                font-size: 11px;
                max-width: 19%;
            }
        }
'''

    # Insert before closing </style>
    style_close = content.find('</style>')
    if style_close != -1 and '@media (max-width: 600px)' not in content:
        content = content[:style_close] + media_query + content[style_close:]

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
    print(f"Fixing canvas rendering and label wrapping...\n")

    for chart_file in all_charts:
        fix_rendering_and_labels(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

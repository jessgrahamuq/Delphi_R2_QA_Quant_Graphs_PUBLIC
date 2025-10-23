#!/usr/bin/env python3
"""
Script to fix the wrapping issue in severity chart controls.
"""

import re
from pathlib import Path

def fix_controls(file_path):
    """Fix the controls layout to prevent wrapping."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace the .controls CSS
    controls_pattern = r'(\.controls\s*\{[^}]*\})'

    new_controls_css = """.controls {
            margin-bottom: 10px;
            padding: 8px 10px;
            background: #f9f9f9;
            border-radius: 4px;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: nowrap;
            justify-content: space-between;
        }"""

    content = re.sub(controls_pattern, new_controls_css, content, flags=re.DOTALL)

    # Make the mode buttons more compact
    mode_button_pattern = r'(\.mode-button\s*\{[^}]*padding:[^;]*;)'
    content = re.sub(
        mode_button_pattern,
        r'.mode-button {\n            background: white;\n            color: #a32035;\n            border: none;\n            padding: 8px 12px;',
        content,
        flags=re.DOTALL
    )

    # Reduce font size for better fit
    mode_button_font_pattern = r'(\.mode-button\s*\{[^}]*font-size:[^;]*;)'
    content = re.sub(
        r'(\.mode-button[^}]*font-size:\s*)\d+px;',
        r'\g<1>13px;',
        content
    )

    # Make toggle button text smaller
    content = re.sub(
        r'(\.toggle-button[^}]*font-size:\s*)\d+px;',
        r'\g<1>13px;',
        content
    )

    # Reduce toggle button padding
    content = re.sub(
        r'(\.toggle-button[^}]*padding:\s*)10px 0px;',
        r'\g<1>8px 0px;',
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
    print(f"Fixing control wrapping issues...\n")

    for chart_file in all_charts:
        fix_controls(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

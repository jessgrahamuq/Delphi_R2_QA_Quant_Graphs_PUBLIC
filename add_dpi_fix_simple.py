#!/usr/bin/env python3
"""
Add DPI fix after medianValuesPlugin closing brace.
"""

from pathlib import Path

def add_dpi_fix(file_path):
    """Add DPI fix after medianValuesPlugin closes."""

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if already has DPI fix
    for line in lines:
        if '// Fix blurry canvas on high-DPI displays' in line:
            print(f"Skipped (already has DPI fix): {file_path.name}")
            return

    dpi_fix_lines = [
        '\n',
        '        // Fix blurry canvas on high-DPI displays\n',
        '        const dpr = window.devicePixelRatio || 1;\n',
        '        const canvas = document.getElementById(\'severityChart\');\n',
        '        const rect = canvas.getBoundingClientRect();\n',
        '        canvas.width = rect.width * dpr;\n',
        '        canvas.height = rect.height * dpr;\n',
        '        ctx.scale(dpr, dpr);\n'
    ]

    # Find the line with "        };" that closes medianValuesPlugin
    # It should be after the plugin definition and before the chart creation
    new_lines = []
    found_plugin_close = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # Look for the closing of medianValuesPlugin
        if not found_plugin_close and line.strip() == '};':
            # Check if this is after medianValues plugin definition
            # Look back to see if we recently saw the plugin
            lookback = ''.join(lines[max(0, i-200):i])
            if 'medianValuesPlugin' in lookback and 'afterDatasetsDraw' in lookback:
                # Add DPI fix after this line
                new_lines.extend(dpi_fix_lines)
                found_plugin_close = True

    if not found_plugin_close:
        print(f"ERROR: Could not find medianValuesPlugin closing in {file_path.name}")
        return

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

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
    print(f"Adding DPI fix after medianValuesPlugin...\n")

    for chart_file in all_charts:
        add_dpi_fix(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

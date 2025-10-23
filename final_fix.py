#!/usr/bin/env python3
"""
Final fix: Apply the working structure from exemplar.
1. Only ctx at the start (no canvas)
2. medianValuesPlugin
3. DPI fix (which defines canvas)
4. Chart creation
5. Event handlers AFTER chart
"""

from pathlib import Path
import re

def fix_chart_file(file_path):
    """Fix a single chart file."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Remove any existing "const canvas = " line that comes before the DPI fix
    # This is the line that comes right before "const ctx"
    content = re.sub(
        r'        const canvas = document\.getElementById\(\'severityChart\'\);\n        const ctx = document\.getElementById\(\'severityChart\'\)\.getContext\(\'2d\'\);',
        r'        const ctx = document.getElementById(\'severityChart\').getContext(\'2d\');',
        content
    )

    # Step 2: Ensure the DPI fix is in the right place and defines canvas
    # Remove any existing DPI fix
    content = re.sub(
        r'\n        //  Fix blurry canvas on high-DPI displays\n        const dpr = window\.devicePixelRatio \|\| 1;\n        const (rect|canvas) = .*?\n        .*?\n        .*?\n        ctx\.scale\(dpr, dpr\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Add DPI fix right before chart creation
    dpi_fix = '''
        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const canvas = document.getElementById('severityChart');
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);

'''

    # Insert before "const chart = new Chart"
    content = re.sub(
        r'(        const chart = new Chart\(ctx,)',
        dpi_fix + r'\1',
        content
    )

    # Step 3: Move mouse event handlers after chart creation
    # First, extract the handlers
    mouse_handler_pattern = r'(\n        // Add mouse move handler for hover interaction\n        const chartCanvas = document\.getElementById\(\'severityChart\'\);\n        const tooltip = document\.getElementById\(\'expertTooltip\'\);.*?chartCanvas\.addEventListener\(\'mouseleave\'.*?\n        \}\);\n)'

    match = re.search(mouse_handler_pattern, content, re.DOTALL)

    if match:
        handlers = match.group(1)
        # Remove from current location
        content = content.replace(handlers, '')

        # Insert right before "// UI Controls"
        content = re.sub(
            r'(\n        // UI Controls)',
            handlers + r'\1',
            content
        )

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed: {file_path.name}")


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
    print(f"Applying final fix...\n")

    for chart_file in all_charts:
        fix_chart_file(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

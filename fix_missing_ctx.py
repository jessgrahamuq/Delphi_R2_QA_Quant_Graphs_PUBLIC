#!/usr/bin/env python3
"""
Fix missing ctx by adding the proper DPI fix code before chart creation.
"""

import re
from pathlib import Path

def fix_missing_ctx(file_path):
    """Add the DPI fix code before chart creation."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The working DPI fix from exemplar
    dpi_fix = '''
        // Fix blurry canvas on high-DPI displays
        const ctx = document.getElementById('severityChart').getContext('2d');
        const dpr = window.devicePixelRatio || 1;
        const canvas = document.getElementById('severityChart');
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
'''

    # Find where chart is created and insert before it if ctx doesn't exist
    if 'const chart = new Chart(ctx,' in content:
        # Check if ctx is already defined before this
        chart_pos = content.find('const chart = new Chart(ctx,')
        before_chart = content[:chart_pos]

        if 'const ctx = ' not in before_chart:
            # Insert the DPI fix right before chart creation
            # Find a good insertion point - after the mouseleave event listener
            if 'chartCanvas.addEventListener(\'mouseleave\'' in before_chart:
                # Insert after this event listener
                pattern = r"(chartCanvas\.addEventListener\('mouseleave'[^}]+\}\);)\s*"
                replacement = r"\1\n" + dpi_fix + "\n        "
                content = re.sub(pattern, replacement, content)
            else:
                # Just insert before chart creation
                content = content.replace(
                    'const chart = new Chart(ctx,',
                    dpi_fix + '\n        const chart = new Chart(ctx,'
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
    print(f"Fixing missing ctx definitions...\n")

    for chart_file in all_charts:
        fix_missing_ctx(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

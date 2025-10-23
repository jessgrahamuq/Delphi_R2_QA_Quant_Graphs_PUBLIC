#!/usr/bin/env python3
"""
Apply the EXACT structure from exemplar: ctx first, then DPI fix without redefining ctx.
"""

import re
from pathlib import Path

def fix_dpi_correct(file_path):
    """Fix DPI with correct structure from exemplar."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The correct pattern from exemplar:
    # 1. const ctx = getContext
    # 2. medianValuesPlugin
    # 3. DPI fix (that uses ctx, doesn't redefine it)

    # Remove the broken DPI fix that redefines ctx
    content = re.sub(
        r'// Fix blurry canvas on high-DPI displays\s*const ctx = document\.getElementById.*?ctx\.scale\(dpr, dpr\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Now find where medianValuesPlugin ends (look for the closing };)
    # and insert the DPI fix RIGHT AFTER it

    dpi_fix_correct = '''
        // Fix blurry canvas on high-DPI displays
        const dpr = window.devicePixelRatio || 1;
        const canvas = document.getElementById('severityChart');
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
'''

    # Find the end of medianValuesPlugin and insert DPI fix after it
    # Pattern: closing of medianValuesPlugin followed by whitespace then either // Track hover or something else
    pattern = r'(const medianValuesPlugin = \{[^}]+afterDatasetsDraw:[^}]+\}\s*\};)\s*\n'

    replacement = r'\1' + dpi_fix_correct + '\n'

    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

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
    print(f"Applying correct DPI fix structure from exemplar...\n")

    for chart_file in all_charts:
        fix_dpi_correct(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

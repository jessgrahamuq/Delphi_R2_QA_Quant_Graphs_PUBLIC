#!/usr/bin/env python3
"""
Script to fix blurry rendering of severity charts in iframes.
"""

import re
from pathlib import Path

def fix_iframe_rendering(file_path):
    """Add CSS to ensure sharp rendering in iframes."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the body CSS and add rendering optimizations
    body_pattern = r'(body\s*\{[^}]*)\}'

    # Check if these properties already exist
    if 'image-rendering' not in content:
        # Add rendering properties to body
        body_replacement = r'\g<1>' + '''
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }'''
        content = re.sub(body_pattern, body_replacement, content)

    # Add canvas rendering optimization
    if 'canvas {' not in content:
        # Insert after the body style
        style_end = content.find('</style>')
        if style_end != -1:
            canvas_style = '''        canvas {
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
        }
'''
            content = content[:style_end] + canvas_style + content[style_end:]

    # Also ensure the chart canvas has proper devicePixelRatio handling in the script
    # Look for Chart.js configuration and add devicePixelRatio
    if 'devicePixelRatio' not in content:
        # Find the Chart options
        chart_pattern = r'(new Chart\([^,]+,\s*\{[^}]*options:\s*\{)'
        if re.search(chart_pattern, content):
            content = re.sub(
                chart_pattern,
                r'\g<1>\n                devicePixelRatio: window.devicePixelRatio || 2,',
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
    print(f"Adding sharp rendering CSS for iframes...\n")

    for chart_file in all_charts:
        fix_iframe_rendering(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

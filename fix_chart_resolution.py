#!/usr/bin/env python3
"""
Script to properly fix Chart.js rendering resolution for sharp display in iframes.
"""

import re
from pathlib import Path

def fix_chart_resolution(file_path):
    """Fix Chart.js to render at proper resolution for high-DPI displays."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Chart.js options section and add devicePixelRatio
    # We need to add it right after "options: {"

    if 'devicePixelRatio' not in content:
        # Add devicePixelRatio to options
        content = re.sub(
            r'(options:\s*\{)',
            r'''\1
                devicePixelRatio: window.devicePixelRatio || 2,''',
            content
        )

    # Also ensure the canvas itself is configured properly
    # Find the canvas element and ensure it has proper attributes
    if '<canvas id="expertChart"' in content:
        # Replace canvas to ensure it's set up correctly
        content = re.sub(
            r'<canvas id="expertChart"[^>]*>',
            r'<canvas id="expertChart" style="width: 100%; height: 100%;">',
            content
        )

    # Add script to force high resolution rendering right after Chart creation
    # Find where the chart is created
    if 'const chart = new Chart(' in content and 'chart.canvas.style' not in content:
        # Add code right after chart creation to ensure proper scaling
        resize_code = '''

        // Force high-resolution rendering
        const dpr = window.devicePixelRatio || 2;
        const canvas = chart.canvas;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        canvas.style.width = rect.width + 'px';
        canvas.style.height = rect.height + 'px';
        const ctx = canvas.getContext('2d');
        ctx.scale(dpr, dpr);
        chart.resize();'''

        # Insert after the chart variable declaration
        content = re.sub(
            r'(const chart = new Chart\([^;]+\);)',
            r'\1' + resize_code,
            content,
            flags=re.DOTALL
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
    print(f"Fixing Chart.js resolution for sharp rendering...\n")

    for chart_file in all_charts:
        fix_chart_resolution(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

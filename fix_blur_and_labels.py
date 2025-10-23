#!/usr/bin/env python3
"""
Script to fix blurry canvas rendering and reduce harm label size.
"""

import re
from pathlib import Path

def fix_blur_and_labels(file_path):
    """Fix canvas blur and reduce harm label size."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Make harm labels much smaller
    content = re.sub(
        r'(\.severity-label\s*\{[^}]*font-size:\s*)\d+px;',
        r'\g<1>11px;',
        content
    )

    # 2. Reduce max-width further
    content = re.sub(
        r'(\.severity-label\s*\{[^}]*max-width:\s*)\d+%;',
        r'\g<1>14%;',
        content
    )

    # 3. Fix the DPI scaling - need to move it AFTER chart creation and use requestAnimationFrame
    # Remove the old DPI scaling code before chart creation
    content = re.sub(
        r'// Fix blurry canvas on high-DPI displays\s*const dpr = window\.devicePixelRatio[^}]+ctx\.scale\(dpr, dpr\);\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # 4. Find where the chart is created and add proper high-DPI handling AFTER it
    if 'const chart = new Chart(ctx,' in content and 'window.addEventListener(\'resize\'' not in content:
        # Find the end of chart options (after the closing braces)
        # We'll add code after the chart creation

        # Add this code right after chart variable is created
        high_dpi_fix = '''

        // Proper high-DPI rendering fix
        function updateChartSize() {
            const dpr = window.devicePixelRatio || 2;
            const canvas = chart.canvas;
            const container = canvas.parentElement;
            const width = container.clientWidth;
            const height = container.clientHeight;

            // Set canvas internal size (scaled by DPR)
            canvas.width = width * dpr;
            canvas.height = height * dpr;

            // Set canvas display size
            canvas.style.width = width + 'px';
            canvas.style.height = height + 'px';

            // Scale the drawing context
            const ctx = canvas.getContext('2d');
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

            // Trigger chart resize/redraw
            chart.resize();
            chart.update('none');
        }

        // Call after initial render
        requestAnimationFrame(() => {
            updateChartSize();
        });

        // Update on window resize
        window.addEventListener('resize', () => {
            requestAnimationFrame(updateChartSize);
        });'''

        # Find a good insertion point - after the chart variable is fully created
        # Look for the closing of the Chart constructor
        chart_pattern = r'(const chart = new Chart\(ctx, \{[^}]+\}\s*\);)'

        # This is complex because of nested braces, so let's find the chart creation more carefully
        # We'll insert after we see "const chart = new Chart" followed by the options closing

        # Simple approach: insert before the medianValuesPlugin definition or before updateChartData function
        if 'function updateChartData()' in content:
            content = content.replace(
                'function updateChartData()',
                high_dpi_fix + '\n\n        function updateChartData()'
            )
        elif '// Update chart when mode changes' in content:
            content = content.replace(
                '// Update chart when mode changes',
                high_dpi_fix + '\n\n        // Update chart when mode changes'
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
    print(f"Fixing canvas blur and reducing label size...\n")

    for chart_file in all_charts:
        fix_blur_and_labels(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

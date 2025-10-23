#!/usr/bin/env python3
"""
Script to fix blurry canvas in Qualtrics iframes by ensuring proper DPI from the start.
"""

import re
from pathlib import Path

def fix_iframe_blur(file_path):
    """Fix canvas blur in Qualtrics iframes with proper initial DPI handling."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any existing high-DPI fix code
    content = re.sub(
        r'// Proper high-DPI rendering fix.*?window\.addEventListener\(\'resize\'[^}]+\}\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Find where we get the canvas context (before chart creation)
    # We need to scale the canvas BEFORE Chart.js initializes

    # Look for where ctx is defined
    if "const ctx = canvas.getContext('2d')" in content or "const ctx = document.getElementById('severityChart').getContext('2d')" in content:

        # Replace the context creation with high-DPI setup
        old_ctx_pattern = r"const ctx = (canvas|document\.getElementById\('severityChart'\))\.getContext\('2d'\);"

        new_ctx_code = """const canvas = document.getElementById('severityChart');

        // Set up high-DPI canvas BEFORE creating chart
        const dpr = window.devicePixelRatio || 2;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        canvas.style.width = rect.width + 'px';
        canvas.style.height = rect.height + 'px';

        const ctx = canvas.getContext('2d');
        ctx.scale(dpr, dpr);"""

        content = re.sub(old_ctx_pattern, new_ctx_code, content)

    # Also add responsive handling for when iframe resizes
    # Find a good place to add resize handler (after chart is created)
    if 'const chart = new Chart(ctx,' in content and 'window.addEventListener(\'load\'' not in content:

        resize_handler = """

        // Handle iframe resize and initial load
        function handleResize() {
            const canvas = document.getElementById('severityChart');
            const dpr = window.devicePixelRatio || 2;
            const rect = canvas.getBoundingClientRect();

            if (rect.width > 0 && rect.height > 0) {
                canvas.width = rect.width * dpr;
                canvas.height = rect.height * dpr;
                canvas.style.width = rect.width + 'px';
                canvas.style.height = rect.height + 'px';

                const ctx = canvas.getContext('2d');
                ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

                if (typeof chart !== 'undefined') {
                    chart.resize();
                }
            }
        }

        // Handle both load and resize events for iframes
        window.addEventListener('load', handleResize);
        window.addEventListener('resize', handleResize);

        // Also try after a short delay for Qualtrics iframes
        setTimeout(handleResize, 100);
        setTimeout(handleResize, 500);"""

        # Insert after updateChartData function or before the mode change listeners
        if 'function updateChartData()' in content:
            content = content.replace(
                'function updateChartData()',
                resize_handler + '\n\n        function updateChartData()'
            )
        elif '// Update chart when mode changes' in content:
            content = content.replace(
                '// Update chart when mode changes',
                resize_handler + '\n\n        // Update chart when mode changes'
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
    print(f"Fixing canvas blur for Qualtrics iframes...\n")

    for chart_file in all_charts:
        fix_iframe_blur(chart_file)

    print(f"\nCompleted! Updated {len(all_charts)} files.")


if __name__ == '__main__':
    main()

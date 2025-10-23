#!/usr/bin/env python3
"""
Move mouse event handlers to AFTER chart creation.
The handlers reference 'chart' so they must come after it's created.
"""

from pathlib import Path
import re

def fix_event_handler_order(file_path):
    """Move event handlers after chart creation."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match the mouse event handlers section
    # From "// Add mouse move handler" to the closing of the mouseleave handler
    event_handlers_pattern = r'(        // Add mouse move handler for hover interaction\n        const chartCanvas = document\.getElementById\(\'severityChart\'\);\n        const tooltip = document\.getElementById\(\'expertTooltip\'\);\n\n        chartCanvas\.addEventListener\(\'mousemove\',.*?chartCanvas\.addEventListener\(\'mouseleave\',.*?\n        \}\);\n\n)'

    match = re.search(event_handlers_pattern, content, re.DOTALL)

    if not match:
        print(f"ERROR: Could not find event handlers in {file_path.name}")
        return

    event_handlers = match.group(1)

    # Remove the event handlers from their current location
    content = content.replace(event_handlers, '')

    # Find the end of chart creation (closing of Chart constructor)
    # Look for the pattern where Chart(...) ends with }); followed by update button handlers
    # We want to insert BEFORE the button handlers

    # Find "// Update mode buttons" or first button event listener
    insert_pattern = r'(        // Update mode buttons|        document\.getElementById\(\'exactBtn\'\)\.addEventListener)'

    match = re.search(insert_pattern, content)
    if match:
        insert_pos = match.start()
        content = content[:insert_pos] + event_handlers + content[insert_pos:]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Fixed: {file_path.name}")
    else:
        print(f"ERROR: Could not find insertion point in {file_path.name}")


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
    print(f"Moving event handlers after chart creation...\n")

    for chart_file in all_charts:
        fix_event_handler_order(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

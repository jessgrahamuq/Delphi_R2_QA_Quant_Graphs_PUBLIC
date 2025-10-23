#!/usr/bin/env python3
"""
Move event handlers to after chart creation.
"""

from pathlib import Path

def move_handlers(file_path):
    """Move event handlers after chart creation."""

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the event handler section
    handler_start = None
    handler_end = None

    for i, line in enumerate(lines):
        if '// Add mouse move handler for hover interaction' in line:
            handler_start = i
        if handler_start is not None and 'chartCanvas.addEventListener(\'mouseleave\'' in line:
            # Find the closing }); of this addEventListener
            for j in range(i, min(i + 10, len(lines))):
                if '});' in lines[j]:
                    handler_end = j + 1  # Include the line after });
                    break
            break

    if handler_start is None or handler_end is None:
        print(f"ERROR: Could not find event handlers in {file_path.name}")
        return

    # Extract the event handler section (including blank line after)
    handler_lines = lines[handler_start:handler_end]

    # Remove from current location
    del lines[handler_start:handler_end]

    # Find where to insert: after the chart closing "        });" and before "        // UI Controls"
    insert_pos = None
    for i, line in enumerate(lines):
        if '// UI Controls' in line:
            insert_pos = i
            break

    if insert_pos is None:
        print(f"ERROR: Could not find insertion point in {file_path.name}")
        return

    # Insert the handlers before "// UI Controls"
    for j, handler_line in enumerate(handler_lines):
        lines.insert(insert_pos + j, handler_line)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

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
    print(f"Moving event handlers...\n")

    for chart_file in all_charts:
        move_handlers(chart_file)

    print(f"\nCompleted!")


if __name__ == '__main__':
    main()

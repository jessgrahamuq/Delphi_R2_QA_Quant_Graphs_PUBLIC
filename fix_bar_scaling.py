#!/usr/bin/env python3
import re
import os
from pathlib import Path

def fix_bar_heights_in_file(filepath):
    """Fix bar heights to use absolute percentage scaling instead of relative scaling."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all distribution bars with their height and percentage
    # Pattern: <div class="distribution-bar" style="height: XXXpx; ... <div class="bar-label"...>XX% (YY)</div>

    # We need to extract the percentage from the bar-label and recalculate the height
    # The pattern is complex because of the nested divs

    modified = False
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Look for distribution-bar lines
        if 'class="distribution-bar"' in line and 'style="height:' in line:
            # Extract current height
            height_match = re.search(r'height:\s*([\d.]+)px', line)
            if not height_match:
                i += 1
                continue

            current_height = float(height_match.group(1))

            # Look ahead for the bar-label line (usually 1-3 lines ahead)
            percentage = None
            for j in range(i + 1, min(i + 5, len(lines))):
                label_match = re.search(r'(\d+)%\s*\(\d+\)', lines[j])
                if label_match:
                    percentage = int(label_match.group(1))
                    break

            if percentage is not None:
                # Calculate new height: percentage% of 80px max height
                # But keep minimum of 3px for visibility
                new_height = max(3.0, (percentage / 100.0) * 80.0)

                # Only modify if the height changed significantly (more than 0.1px difference)
                if abs(new_height - current_height) > 0.1:
                    # Replace the height in the line
                    lines[i] = re.sub(
                        r'height:\s*[\d.]+px',
                        f'height: {new_height}px',
                        line
                    )
                    modified = True

        i += 1

    if modified:
        new_content = '\n'.join(lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = Path('/Users/universityofqueensland/Desktop/Delphi_R2_QA_Quant_Graphs_PUBLIC')

    # Process Responsibility charts
    resp_dir = base_dir / 'Resp_Charts'
    vuln_dir = base_dir / 'Vuln_Charts'

    print("Processing Responsibility Charts...")
    resp_files = list(resp_dir.glob('*.html'))
    for filepath in resp_files:
        if fix_bar_heights_in_file(filepath):
            print(f"  Fixed: {filepath.name}")
        else:
            print(f"  No changes: {filepath.name}")

    print("\nProcessing Vulnerability Charts...")
    vuln_files = list(vuln_dir.glob('*.html'))
    for filepath in vuln_files:
        if fix_bar_heights_in_file(filepath):
            print(f"  Fixed: {filepath.name}")
        else:
            print(f"  No changes: {filepath.name}")

    print(f"\nTotal files processed: {len(resp_files) + len(vuln_files)}")

if __name__ == '__main__':
    main()

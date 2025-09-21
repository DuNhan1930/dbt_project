import os
from pathlib import Path

input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped.jsonl")
output_dir = Path("/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped")
lines_per_file = 1000

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

file_count = 0
current_lines = []

with open(input_file, "r", encoding="utf-8") as infile:
    for i, line in enumerate(infile, 1):
        current_lines.append(line)
        if i % lines_per_file == 0:
            output_path = os.path.join(output_dir, f"tld_grouped_part_{file_count}.jsonl")
            with open(output_path, "w", encoding="utf-8") as outfile:
                outfile.writelines(current_lines)
            print(f"Written: {output_path} ({len(current_lines)} lines)")
            current_lines = []
            file_count += 1

    # Write any remaining lines
    if current_lines:
        output_path = os.path.join(output_dir, f"tld_grouped_part_{file_count}.jsonl")
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.writelines(current_lines)
        print(f"Written: {output_path} ({len(current_lines)} lines)")

print(f"\nDone! Total files created: {file_count + 1}")

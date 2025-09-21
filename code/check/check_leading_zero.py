import json
import re
from pathlib import Path

input_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/product_name.json")
log_every = 100000  # Log progress every 100k lines
check_field = ""

# Metrics
total_lines = 0
violations = 0

def find_all(obj):
    """Recursively find all check_field values in the object."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == check_field:
                yield v
            else:
                yield from find_all(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from find_all(item)

def has_leading_zero(value):
    """Check if the value has a leading zero but is not '0' itself."""
    return isinstance(value, str) and re.match(r'^0\d+', value)

with open(input_path, 'r', encoding='utf-8') as infile:
    for line in infile:
        total_lines += 1

        try:
            record = json.loads(line)
            for num in find_all(record):
                if has_leading_zero(num):
                    print(f"[Violation] Line {total_lines}: {check_field} has leading zero → {num}")
                    violations += 1
                    break  # Report only once per line for brevity
        except json.JSONDecodeError as e:
            print(f"[Error] Line {total_lines}: JSON decode failed - {e}")

        if total_lines % log_every == 0:
            print(f"[Progress] Processed {total_lines} lines... Violations so far: {violations}")

# Final report
print(f"\nFinished scanning.")
print(f"Total lines processed: {total_lines}")
print(f"Total lines with {check_field} leading-zero violations: {violations}")

import json
from collections import defaultdict
from pathlib import Path

# Input file path
input_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary.json")

unique_ips = set()
null_counts = defaultdict(int)
total_lines = 0

with open(input_path, "r") as f:
    for line in f:
        try:
            record = json.loads(line)
            total_lines += 1

            # Count unique IPs
            ip = record.get("ip")
            if ip:
                unique_ips.add(ip)
            else:
                null_counts["ip"] += 1

            for key in record:
                value = record[key]
                if value in [None, "", [], {}, False]:
                    null_counts[key] += 1

        except Exception as e:
            print(f"Error parsing line {total_lines + 1}: {e}")
            continue

# Output results
print(f"\nTotal lines: {total_lines}")
print(f"Unique IPs: {len(unique_ips)}\n")
print("Null/Empty Counts Per Field:")
for key, count in sorted(null_counts.items()):
    print(f"  {key}: {count}")

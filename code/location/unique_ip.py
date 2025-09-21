import json
from pathlib import Path

# Input and output paths
input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/summary.json")
output_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/unique_ip.json")

unique_ips = set()
null_ip_count = 0
total_lines = 0

with open(input_file, "r") as f:
    for line in f:
        try:
            record = json.loads(line)
            total_lines += 1
            print(total_lines)

            ip = record.get("ip")

            if ip and isinstance(ip, str) and ip.strip():
                unique_ips.add(ip.strip())
            else:
                null_ip_count += 1

        except json.JSONDecodeError as e:
            print(f"JSON error at line {total_lines + 1}: {e}")
            continue

# Save as JSON Lines format — one JSON object per line
with open(output_file, "w") as f:
    for ip in sorted(unique_ips):
        f.write(json.dumps({"ip": ip}) + "\n")

# Print results
print(f"Total lines processed: {total_lines}")
print(f"Unique non-null IPs found: {len(unique_ips)}")
print(f"Records with missing/null IPs: {null_ip_count}")
print(f"Unique IPs saved to: {output_file} in JSON Lines format.")
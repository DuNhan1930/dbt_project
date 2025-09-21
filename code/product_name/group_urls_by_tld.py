import json
import re
from collections import defaultdict
from urllib.parse import urlparse
from pathlib import Path

# Input and output files
input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/filtered_grouped.json")
output_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped.jsonl")

# TLD extraction using domain
def extract_tld(url):
    try:
        netloc = urlparse(url).netloc
        match = re.search(r"\.(\w+)$", netloc)
        if match:
            return match.group(1).lower()
    except:
        pass
    return "unknown"

# Accumulate global TLD summary
global_tld_count = defaultdict(int)

# Open output JSONL file for writing
with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    for line in f_in:
        tld_grouped = defaultdict(list)  # reset for each product

        try:
            record = json.loads(line.strip())
            pid = record.get('product_id')
            collection = record.get('collection', [])
            urls = record.get("current_url", [])

            for url in urls:
                tld = extract_tld(url)
                tld_grouped[tld].append(url)
                global_tld_count[tld] += 1

            # Write each product record as one line in JSONL
            f_out.write(json.dumps({
                "product_id": pid,
                "current_url": tld_grouped,
                "collections": collection
            }, ensure_ascii=False) + "\n")

        except json.JSONDecodeError as e:
            print(f"Skipping invalid line due to JSON error: {e}")

# Global TLD summary
print("\nTLD Summary:")
print(f"Total unique TLDs found: {len(global_tld_count)}\n")
for tld, count in sorted(global_tld_count.items(), key=lambda x: -x[1]):
    print(f".{tld}: {count} URLs")

print(f"\nJSONL output saved to: {output_file}")

import json
from pathlib import Path

input_file = Path("/media/dunhan/Extreme SSD/Glamira_Data/tld_grouped_test.json")

with open(input_file, "r") as infile:
    records = json.load(infile)  # Top-level is a dict
    for record in records:
        tlds = record.get("current_url", {})
        for tld in tlds:
            url = tlds.get(tld, [])
            print(tld)
            print(url)
import json
import IP2Location
import csv
from pathlib import Path

# Load IP2Location DB11
db = IP2Location.IP2Location("/home/dunhan/PycharmProjects/Glamira_Project5/IP2LOCATION-LITE-DB11.BIN")

# File paths
input_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/unique_ip.json")
output_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/location.json")
fail_path = Path("/media/dunhan/Extreme SSD/Glamira_Data/fail_convert.csv")

# Open output files
with open(input_path, "r") as infile, \
     open(output_path, "w") as locfile, \
     open(fail_path, "w", newline='') as failfile:

    fail_writer = csv.DictWriter(failfile, fieldnames=["ip", "error"])
    fail_writer.writeheader()

    success_count = 0
    fail_count = 0

    for line in infile:
        try:
            record = json.loads(line)
            ip = record.get("ip", "")
            rec = db.get_all(ip)
            location = {
                "ip": ip,
                "country_short": rec.country_short,
                "country_long": rec.country_long,
                "region": rec.region,
                "city": rec.city,
                "latitude": rec.latitude,
                "longitude": rec.longitude,
                "zip_code": rec.zipcode,
                "time_zone": rec.timezone
            }
            locfile.write(json.dumps(location) + "\n")
            print(f"[SUCCESS] {ip}")
            success_count += 1
            print(success_count)
        except Exception as e:
            ip = record.get("ip", "N/A")
            fail_writer.writerow({"ip": ip, "error": str(e)})
            print(f"[FAIL]    {ip} - {e}")
            fail_count += 1

print(f"\nConversion finished. {success_count} IPs succeeded, {fail_count} failed.")

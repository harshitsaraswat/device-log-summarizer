"""Creates device_telemetry.csv with random data plus a few bad rows."""
import csv
import random

random.seed(42)
DEVICES = {"DEV_A": 70, "DEV_B": 88, "DEV_C": 65, "DEV_D": 58, "DEV_E": 76}

rows = []
for device, base_temp in DEVICES.items():
    for _ in range(8):
        status = random.choices(["ACTIVE", "WARNING", "ERROR"], [70, 20, 10])[0]
        rows.append([device, status, round(random.uniform(base_temp - 6, base_temp + 6), 1)])

# Bad data the program must survive
rows += [["DEV_C", "WARNING", "abc"], ["DEV_D", "ERROR", ""], ["", "ACTIVE", "50"]]

with open("device_telemetry.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["device_id", "status", "temperature"])
    writer.writerows(rows)
print(f"Wrote {len(rows)} rows to device_telemetry.csv")

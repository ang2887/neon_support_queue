# visualise_usage.py v5 (no regex)

import matplotlib.pyplot as plt
from datetime import datetime

THRESHOLD_STORAGE_GB = 0.45
THRESHOLD_COMPUTE_CU = 180
LOG_FILE = "neon_monitor.log"

dates, storage, compute = [], [], []

with open(LOG_FILE, "r") as file:
    for line in file:
        # Only handle lines starting with a timestamp
        if not line[:4].isdigit():
            continue
        if "Storage" in line and "Compute" in line:
            try:
                # Extract timestamp
                timestamp_str = line.split(" [")[0]
                dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

                # Extract values
                start = line.index("Storage:")
                usage_part = line[start:]
                parts = usage_part.replace("Storage:", "").replace("Compute:", "").split("|")

                storage_val = float(parts[0].strip().replace("GB", ""))
                compute_val = float(parts[1].strip().replace("CU", ""))

                dates.append(dt)
                storage.append(storage_val)
                compute.append(compute_val)

            except Exception as e:
                print(f"⚠️ Skipping line due to error: {e}")

# Show chart
if not dates:
    print("⚠️ No usage data found in the log.")
    exit()

plt.figure(figsize=(10, 5))
plt.plot(dates, storage, label="Storage (GB)")
plt.plot(dates, compute, label="Compute (CU)")

plt.axhline(THRESHOLD_STORAGE_GB, color="red", linestyle="--", label="Storage Threshold")
plt.axhline(THRESHOLD_COMPUTE_CU, color="orange", linestyle="--", label="Compute Threshold")

plt.xlabel("Date")
plt.ylabel("Usage")
plt.title("Neon Usage Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
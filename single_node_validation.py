import pandas as pd
import time
import random
import os

# Save path
file_path = os.path.join(os.path.expanduser("~"), "Desktop", "single_node_data.csv")

data = []

# Frost Threshold
FROST_THRESHOLD = 2.0

print("Single-node validation started")
print("Simulated serial output format:")
print("timestamp,temp,hum,pres,frost_status")
print("Press Ctrl+C to stop")
print("Saving to:", file_path)

while True:
# Simulated sensor data
# Temperature setting is slightly lower to facilitate frost detection testing
    temp = round(3 + random.uniform(-4, 6), 2)
    hum = round(70 + random.uniform(-10, 15), 2)
    pres = round(1010 + random.uniform(-5, 5), 2)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

# If the temperature is below or equal to the threshold, frost may have occurred
    if temp <= FROST_THRESHOLD:
        frost_status = "FROST_WARNING"
    else:
        frost_status = "NORMAL"

# Simulated serial port output format
    serial_output = f"{timestamp},Temp:{temp},Hum:{hum},Pres:{pres},Status:{frost_status}"
    print(serial_output)

# Save data
    data.append([timestamp, temp, hum, pres, frost_status])

    df = pd.DataFrame(
        data,
        columns=["timestamp", "temperature_C", "humidity_percent", "pressure_hPa", "frost_status"]
    )

    df.to_csv(file_path, index=False)

    time.sleep(1)
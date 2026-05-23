import pandas as pd
import matplotlib.pyplot as plt
import os

# Read CSV
file_path = os.path.join(os.path.expanduser("~"), "Desktop", "single_node_data.csv")
df = pd.read_csv(file_path)

# Convert time format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Temperature graph (with frost detection)
frost_points = df[df["frost_status"] == "FROST_WARNING"]

plt.figure(figsize=(12, 6))

plt.plot(df["timestamp"], df["temperature_C"], label="Temperature (°C)")

plt.scatter(
    frost_points["timestamp"],
    frost_points["temperature_C"],
    color="red",
    label="Frost Warning",
    zorder=3
)

plt.axhline(y=2, color="gray", linestyle="--", label="Frost Threshold (2°C)")

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Single Node Temperature with Frost Detection")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# Humidity graph
plt.figure(figsize=(12, 6))

plt.plot(df["timestamp"], df["humidity_percent"], label="Humidity (%)")

plt.xlabel("Time")
plt.ylabel("Humidity (%)")
plt.title("Single Node Humidity Over Time")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# Barometric Pressure Chart
plt.figure(figsize=(12, 6))

plt.plot(df["timestamp"], df["pressure_hPa"], label="Pressure (hPa)")

plt.xlabel("Time")
plt.ylabel("Pressure (hPa)")
plt.title("Single Node Pressure Over Time")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
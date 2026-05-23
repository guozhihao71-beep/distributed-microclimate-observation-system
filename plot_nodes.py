import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = os.path.join(os.path.expanduser("~"), "Desktop", "multi_node_environment.csv")
df = pd.read_csv(file_path)

# Time to Format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Antifreeze detection threshold
FROST_THRESHOLD = 2.0

# Add antifreeze test results
df["frost_status"] = df["temperature"].apply(
    lambda temp: "FROST_WARNING" if temp <= FROST_THRESHOLD else "NORMAL"
)


# Temperature graph
plt.figure(figsize=(12, 6))

for node_id in df["node_id"].unique():
    node_data = df[df["node_id"] == node_id]
    plt.plot(node_data["timestamp"], node_data["temperature"], label=node_id)

# Mark frost points
frost_points = df[df["frost_status"] == "FROST_WARNING"]

plt.scatter(
    frost_points["timestamp"],
    frost_points["temperature"],
    color="red",
    label="Frost Warning",
    zorder=3
)

# Frost Threshold Line
plt.axhline(
    y=FROST_THRESHOLD,
    color="gray",
    linestyle="--",
    label="Frost Threshold (2°C)"
)

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Multi-node Temperature with Frost Detection")
plt.xticks(df["timestamp"][::40], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# Humidity graph
plt.figure(figsize=(12, 6))

for node_id in df["node_id"].unique():
    node_data = df[df["node_id"] == node_id]
    plt.plot(node_data["timestamp"], node_data["humidity"], label=node_id)

plt.xlabel("Time")
plt.ylabel("Humidity (%)")
plt.title("Multi-node Humidity")
plt.xticks(df["timestamp"][::40], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# Barometric Pressure Chart
plt.figure(figsize=(12, 6))

for node_id in df["node_id"].unique():
    node_data = df[df["node_id"] == node_id]
    plt.plot(node_data["timestamp"], node_data["pressure"], label=node_id)

plt.xlabel("Time")
plt.ylabel("Pressure (hPa)")
plt.title("Multi-node Pressure")
plt.xticks(df["timestamp"][::40], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
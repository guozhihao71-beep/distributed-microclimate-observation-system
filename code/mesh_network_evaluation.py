import pandas as pd
import matplotlib.pyplot as plt
import os

# Read raw Mesh data
file_path = os.path.join(os.path.expanduser("~"), "Desktop", "mesh_realtime_raw.csv")
df = pd.read_csv(file_path)

# Time format conversion
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Communication latency test; data consistency between nodes; 
# standard deviation of temperature of different nodes at the same time point

received_df = df[df["status"] == "Received"]

avg_delay = received_df["delay_ms"].mean()
max_delay = received_df["delay_ms"].max()
min_delay = received_df["delay_ms"].min()

print("Communication Delay")
print("Average delay:", round(avg_delay, 2), "ms")
print("Max delay:", max_delay, "ms")
print("Min delay:", min_delay, "ms")


# Packet loss rate test

total_packets = len(df)
lost_packets = len(df[df["status"] == "Lost"])
received_packets = len(df[df["status"] == "Received"])

packet_loss_rate = lost_packets / total_packets * 100

print("\n Packet Loss ")
print("Total packets:", total_packets)
print("Received packets:", received_packets)
print("Lost packets:", lost_packets)
print("Packet loss rate:", round(packet_loss_rate, 2), "%")


# Packet loss rate per node;Lost packets / Total packets × 100%

print("\n Packet Loss Rate by Node ")

node_loss = df.groupby("node_id")["status"].apply(
    lambda x: (x == "Lost").sum() / len(x) * 100
)

print(node_loss)


# Data Consistency Between Nodes
# Here, consistency is represented by the standard deviation of temperatures at different nodes at the same time point.
# The smaller the standard deviation, the more consistent the data is between nodes.

consistency = received_df.groupby("timestamp")["temperature"].std()

avg_consistency = consistency.mean()

print("\n Data Consistency")
print("Average inter-node temperature standard deviation:", round(avg_consistency, 2), "°C")


# Network stability; how many nodes successfully received data at each time point; at each time point, 4 packets should be received. If only 3 or fewer are received, it indicates packet loss
# Use the number of successfully received data packets at each time point to judge network stability.

stability = df.groupby("timestamp")["status"].apply(
    lambda x: (x == "Received").sum()
)

print("\nNetwork Stability ")
print("Average received packets per timestamp:", round(stability.mean(), 2))
print("Expected packets per timestamp: 4")


# Communication Delay Graph

plt.figure(figsize=(12, 6))

plt.plot(received_df["timestamp"], received_df["delay_ms"], label="Delay (ms)")

plt.xlabel("Time")
plt.ylabel("Delay (ms)")
plt.title("Mesh Communication Delay Over Time")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# Packet loss rate per node

plt.figure(figsize=(8, 5))

node_loss.plot(kind="bar")
node_loss = node_loss.reindex(df["node_id"].unique(), fill_value=0)
plt.xlabel("Node ID")
plt.ylabel("Packet Loss Rate (%)")
plt.title("Packet Loss Rate by Node")
plt.tight_layout()
plt.show()


# Network stability graph

plt.figure(figsize=(12, 6))

plt.plot(stability.index, stability.values, label="Received Packets per Timestamp")

plt.axhline(y=4, linestyle="--", label="Expected Packets")

plt.xlabel("Time")
plt.ylabel("Number of Received Packets")
plt.title("Mesh Network Stability")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# Data consistency graph between nodes

plt.figure(figsize=(12, 6))

plt.plot(consistency.index, consistency.values, label="Inter-node Temperature Std")

plt.xlabel("Time")
plt.ylabel("Temperature Standard Deviation (°C)")
plt.title("Inter-node Data Consistency")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


#Delay distribution map
plt.figure(figsize=(12, 6))

plt.hist(
    received_df["delay_ms"],
    bins=20,              #Divided into 20 intervals
    edgecolor="black"
)

plt.xlabel("Delay (ms)")
plt.ylabel("Frequency")
plt.title("Mesh Communication Delay Distribution")

plt.tight_layout()
plt.show()
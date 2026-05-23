import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 保存路径：桌面
file_path = os.path.join(os.path.expanduser("~"), "Desktop", "multi_node_environment.csv")

# 4个节点：node_id, x, y, 温度偏移, 湿度偏移, 气压偏移
nodes = [
    {"node_id": "Node_A", "x": 0,  "y": 0,  "temp_offset": -3.0, "hum_offset": 8.0,  "pres_offset": -1.0},
    {"node_id": "Node_B", "x": 10, "y": 0,  "temp_offset": -1.0, "hum_offset": 4.0,  "pres_offset": -0.5},
    {"node_id": "Node_C", "x": 0,  "y": 10, "temp_offset": 1.0,  "hum_offset": -2.0, "pres_offset": 0.5},
    {"node_id": "Node_D", "x": 10, "y": 10, "temp_offset": 2.5,  "hum_offset": -5.0, "pres_offset": 1.0},
]

data = []

# 模拟从凌晨开始，每5分钟一条，持续10小时
start_time = datetime(2026, 4, 27, 0, 0, 0)
num_steps = 120
interval = 5

for i in range(num_steps):
    timestamp = start_time + timedelta(minutes=i * interval)

    hour = timestamp.hour + timestamp.minute / 60

    # 温度：夜间低，白天高
    temp_cycle = 6 * np.sin((2 * np.pi / 24) * (hour - 6))
    base_temp = 8 + temp_cycle

    # 湿度：通常夜间高，白天降低，所以和温度大致相反
    hum_cycle = -10 * np.sin((2 * np.pi / 24) * (hour - 6))
    base_hum = 65 + hum_cycle

    # 气压：变化较小
    pres_cycle = 2 * np.sin((2 * np.pi / 24) * (hour - 3))
    base_pres = 1010 + pres_cycle

    for node in nodes:
        temp_noise = np.random.normal(0, 0.4)
        hum_noise = np.random.normal(0, 1.5)
        pres_noise = np.random.normal(0, 0.3)

        temperature = base_temp + node["temp_offset"] + temp_noise
        humidity = base_hum + node["hum_offset"] + hum_noise
        pressure = base_pres + node["pres_offset"] + pres_noise

        # 限制湿度范围 0–100%
        humidity = max(0, min(100, humidity))

        data.append([
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            node["node_id"],
            node["x"],
            node["y"],
            round(temperature, 2),
            round(humidity, 2),
            round(pressure, 2)
        ])

df = pd.DataFrame(
    data,
    columns=["timestamp", "node_id", "x", "y", "temperature", "humidity", "pressure"]
)

df.to_csv(file_path, index=False)

print("CSV saved to:", file_path)
print(df.head())
print("Total rows:", len(df))
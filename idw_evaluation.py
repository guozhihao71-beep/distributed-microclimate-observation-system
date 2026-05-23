import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Read the processed data
file_path = os.path.join(os.path.expanduser("~"), "Desktop", "mesh_realtime_processed.csv")
df = pd.read_csv(file_path)

# Only use successfully received data
df = df[df["status"] == "Received"]
df = df.dropna(subset=["temperature_smooth", "humidity_smooth", "pressure_smooth"])

# 时间格式转换
df["timestamp"] = pd.to_datetime(df["timestamp"])

# IDW function
def idw_predict(x, y, known_points, value_column, power=2):
    numerator = 0
    denominator = 0

    for _, row in known_points.iterrows():
        distance = np.sqrt((x - row["x"])**2 + (y - row["y"])**2)

        if distance == 0:
            return row[value_column]

        weight = 1 / (distance ** power)
        numerator += weight * row[value_column]
        denominator += weight

    return numerator / denominator


# Leave-One-Out Evaluation Function
def evaluate_idw(value_column):
    results = []

    for timestamp, group in df.groupby("timestamp"):

        # At least 3 points are needed to make an effective prediction.
        if len(group) < 3:
            continue

        for _, target in group.iterrows():

            # target node
            target_node = target["node_id"]
            actual_value = target[value_column]

            # Predict the current node using other nodes.
            known_points = group[group["node_id"] != target_node]

            predicted_value = idw_predict(
                target["x"],
                target["y"],
                known_points,
                value_column
            )

            error = predicted_value - actual_value
            abs_error = abs(error)
            squared_error = error ** 2

            results.append([
                timestamp,
                target_node,
                actual_value,
                predicted_value,
                error,
                abs_error,
                squared_error
            ])

    result_df = pd.DataFrame(
        results,
        columns=[
            "timestamp",
            "node_id",
            "actual",
            "predicted",
            "error",
            "absolute_error",
            "squared_error"
        ]
    )

    mae = result_df["absolute_error"].mean()
    rmse = np.sqrt(result_df["squared_error"].mean())

    return result_df, mae, rmse


# Evaluate temperature, humidity, and air pressure separately
metrics = []

for column, name in [
    ("temperature_smooth", "Temperature"),
    ("humidity_smooth", "Humidity"),
    ("pressure_smooth", "Pressure")
]:
    result_df, mae, rmse = evaluate_idw(column)

    print("\n==============================")
    print(name)
    print("MAE:", round(mae, 3))
    print("RMSE:", round(rmse, 3))

    metrics.append([name, mae, rmse])

    # Save the prediction results for each variable
    output_path = os.path.join(os.path.expanduser("~"), "Desktop", f"idw_{name.lower()}_evaluation.csv")
    result_df.to_csv(output_path, index=False)


#Save the overall evaluation results
metrics_df = pd.DataFrame(metrics, columns=["Variable", "MAE", "RMSE"])

metrics_path = os.path.join(os.path.expanduser("~"), "Desktop", "idw_evaluation_metrics.csv")
metrics_df.to_csv(metrics_path, index=False)

print("\nEvaluation metrics saved to:", metrics_path)
print(metrics_df)

# Draw a comparison chart of MAE and RMSE
plt.figure(figsize=(8, 5))

x = np.arange(len(metrics_df["Variable"]))
width = 0.35

plt.bar(x - width/2, metrics_df["MAE"], width, label="MAE")
plt.bar(x + width/2, metrics_df["RMSE"], width, label="RMSE")

plt.xticks(x, metrics_df["Variable"])
plt.ylabel("Error")
plt.title("IDW Model Evaluation: MAE and RMSE")
plt.legend()
plt.tight_layout()
plt.show()
# distributed-microclimate-observation-system

This repository contains supplementary Python scripts and CSV datasets used in the thesis project:

**Distributed Microclimate Observation System for Frost Risk Monitoring**

## Repository Contents

- `code/`: Python scripts for sensor data simulation, data visualisation, Mesh network evaluation, IDW heatmap generation, and IDW model evaluation.
- `data/`: CSV datasets generated during the simulation and data processing stages.

## Important Note

The uploaded CSV files are simulation-based development data. They were used to test data processing, Mesh communication evaluation, frost warning logic, and IDW spatial interpolation. They should not be interpreted as final field measurement results.

## Python Scripts

The main scripts include:

- `single_node_validation.py`: Simulates single-node sensor data and frost warning logic.
- `plot_single_node.py`: Plots single-node temperature, humidity, and pressure data.
- `simulate_node.py`: Generates simulated multi-node environmental data.
- `plot_nodes.py`: Visualises multi-node temperature, humidity, pressure, and frost warning points.
- `mesh_idw_heatmap.py`: Generates IDW heatmaps for temperature, humidity, and pressure.
- `mesh_network_evaluation.py`: Evaluates Mesh communication delay, packet loss rate, network stability, and inter-node data consistency.
- `idw_evaluation.py`: Evaluates IDW interpolation performance using MAE and RMSE.

## Requirements

The scripts were developed using Python 3 with the following libraries:

- pandas
- numpy
- matplotlib

## Citation

This repository is provided as supplementary material for the thesis project.Supplementary Python scripts and CSV datasets for the Distributed Microclimate Observation System thesis project.

# src/visualize/visualize_data.py

import pandas as pd
import matplotlib.pyplot as plt

def visualize_data(file_path, timestamp_col='timestamp', value_col='value', anomaly_col='anomaly', plot_type='line'):
    """Visualize the data and highlight anomalies."""
    try:
        # Load the data
        data = pd.read_csv(file_path)
        data[timestamp_col] = pd.to_datetime(data[timestamp_col])  # Ensure proper datetime format
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if plot_type == 'line':
            ax.plot(data[timestamp_col], data[value_col], label="Value")
        elif plot_type == 'scatter':
            ax.scatter(data[timestamp_col], data[value_col], label="Value")
        else:
            raise ValueError("Unsupported plot type. Use 'line' or 'scatter'.")
        
        # Highlight anomalies
        ax.scatter(data[data[anomaly_col] == 1][timestamp_col], 
                   data[data[anomaly_col] == 1][value_col], 
                   color='red', label="Anomaly", zorder=5)
        
        ax.set_xlabel("Timestamp")
        ax.set_ylabel(value_col)
        ax.set_title(f"Anomaly Detection Visualization")
        ax.legend()
        
        # Show plot
        plt.show()

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while visualizing data: {e}")

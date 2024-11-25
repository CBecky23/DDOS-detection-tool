import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def load_data(file_path, timestamp_col):
    """Load and preprocess data."""
    try:
        data = pd.read_csv(file_path)
        data[timestamp_col] = pd.to_datetime(data[timestamp_col])
        return data
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise RuntimeError(f"File is empty: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def plot_data(data, timestamp_col, value_col, anomaly_col, plot_type, ax, **kwargs):
    """Generate the plot."""
    if plot_type == 'line':
        ax.plot(data[timestamp_col], data[value_col], label="Value", **kwargs)
    elif plot_type == 'scatter':
        ax.scatter(data[timestamp_col], data[value_col], label="Value", **kwargs)
    else:
        raise ValueError("Unsupported plot type. Use 'line' or 'scatter'.")
    
    # Highlight anomalies
    ax.scatter(data[data[anomaly_col] == 1][timestamp_col], 
               data[data[anomaly_col] == 1][value_col], 
               color='red', label="Anomaly", zorder=5)

def save_plot(fig, save_path):
    """Save the plot to a file."""
    try:
        fig.savefig(save_path)
        print(f"Plot saved to {save_path}")
    except Exception as e:
        raise RuntimeError(f"Error saving plot: {e}")


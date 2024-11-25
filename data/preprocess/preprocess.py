# data/preprocess/preprocess.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import os

def load_data(file_path):
    """Load data from a CSV file."""
    data = pd.read_csv(file_path)
    return data

def clean_data(data):
    """Clean the data by handling missing values and invalid data."""
    # Drop rows with any missing values
    data.dropna(inplace=True)

    # Drop duplicate rows
    data.drop_duplicates(inplace=True)

def preprocess_data(file_path):
    """Preprocess the data by loading, cleaning, and adding a target column."""
    data = load_data(file_path)
    clean_data(data)
    
    # Example preprocessing steps
    # Add a target column for demonstration purposes
    data['target'] = (data['protocol'] == 6).astype(int)  # Example target: 1 if protocol is TCP (6), else 0
    
    # Drop non-numerical columns
    data = data.drop(columns=['timestamp', 'src_ip', 'dst_ip', 'flags'])
    
    # Save the preprocessed data to processed_data.csv
    processed_data_path = os.path.join(os.path.dirname(file_path), 'processed_data.csv')
    data.to_csv(processed_data_path, index=False)
    return processed_data_path
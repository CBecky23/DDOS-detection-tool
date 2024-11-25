# src/detection/ml_detection.py
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_processed_data(file_path):
    """Load processed data for training."""
    return pd.read_csv(file_path)

def train_model(file_path):
    """Train a machine learning model using the data from the specified file path."""
    data = pd.read_csv(file_path)
    if 'target' not in data.columns:
        raise ValueError("The 'target' column is missing from the data.")
    
    X = data.drop(columns=['target'])
    y = data['target']
    
    model = RandomForestClassifier()
    model.fit(X, y)
    
    joblib.dump(model, 'models/trained_model.pkl')
    print("Model trained and saved to models/trained_model.pkl")

def predict_anomaly(file_path):
    """Predict anomalies using the trained model."""
    data = pd.read_csv(file_path)
    if 'target' in data.columns:
        data = data.drop(columns=['target'])  # Exclude the target column
    
    model = joblib.load('models/trained_model.pkl')
    
    predictions = model.predict(data)
    print("Anomaly predictions:", predictions)
    
    # Save the predictions to anomaly_detected.csv
    anomaly_detected_path = os.path.join(os.path.dirname(file_path), 'anomaly_detected.csv')
    data['anomaly'] = predictions
    data.to_csv(anomaly_detected_path, index=False)
    print(f"Anomaly detection results saved to {anomaly_detected_path}")
    
    return predictions

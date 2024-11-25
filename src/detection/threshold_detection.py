# src/detection/threshold_detection.py
import json
import numpy as np
from datetime import datetime
from src.utils.detection_log import log_detection
import smtplib
from email.mime.text import MIMEText
import os

# Initial configuration
THRESHOLD_PACKET_RATE = 100  # Base threshold
ALERT_RECIPIENTS = ["admin@example.com"]
HISTORICAL_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'historical_packet_rates.json')

# Load historical data from JSON file
def load_historical_data():
    try:
        with open(HISTORICAL_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Update historical data with new packet rate
def update_historical_data(packet_rate, src_ip):
    """Update historical data with the new packet rate."""
    if os.path.exists(HISTORICAL_DATA_FILE):
        with open(HISTORICAL_DATA_FILE, 'r') as f:
            historical_data = json.load(f)
    else:
        historical_data = {"historical_data": []}

    new_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "packet_rate": packet_rate,
        "src_ip": src_ip
    }
    historical_data["historical_data"].append(new_entry)

    with open(HISTORICAL_DATA_FILE, 'w') as f:
        json.dump(historical_data, f, indent=4)

# Calculate dynamic threshold based on historical data
def calculate_dynamic_threshold(historical_data):
    if len(historical_data) < 10:  # Need at least 10 data points for statistics
        return THRESHOLD_PACKET_RATE
    
    packet_rates = [entry['packet_rate'] for entry in historical_data]
    mean = np.mean(packet_rates)
    std_dev = np.std(packet_rates)
    
    # Dynamic threshold: mean + 2 * standard deviation
    dynamic_threshold = mean + 2 * std_dev
    return dynamic_threshold

def send_alert(src_ip, packet_rate):
    """Send an email alert when a DDoS attack is detected."""
    sender_email = "youremail@example.com"
    subject = f"DDoS Attack Alert from {src_ip}"
    body = f"DDoS Detected! Source IP: {src_ip}, Packet Rate: {packet_rate}."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(ALERT_RECIPIENTS)

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, 'yourpassword')  # Use environment variables for better security
        server.send_message(msg)

def threshold_detection(packet_rate, src_ip):
    """Detect anomalies based on packet rate and source IP."""
    # Add your detection logic here
    print(f"Running threshold detection with packet_rate={packet_rate} and src_ip={src_ip}")
    update_historical_data(packet_rate, src_ip)
    historical_data = load_historical_data()
    dynamic_threshold = calculate_dynamic_threshold(historical_data)

    if packet_rate > dynamic_threshold:
        print(f"DDoS Detected! Packet Rate: {packet_rate} exceeds threshold: {dynamic_threshold}")
        log_detection(src_ip, packet_rate)
        update_historical_data(packet_rate, src_ip)
        send_alert(src_ip, packet_rate)  # Send alert to admin
        return True
    
    update_historical_data(packet_rate, src_ip)  # Always update historical data
    return False

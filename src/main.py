import sys
import os
import argparse
import logging
from src.utils.config import Config
from src.utils.detection_log import log_detection
from src.capture.packet_sniffer import start_sniffing
from data.preprocess.preprocess import preprocess_data
from src.detection.threshold_detection import threshold_detection
from src.detection.ml_detection import train_model, predict_anomaly
from src.filtering.ip_filter import check_and_filter_ip
from visualize_data import visualize_data  

# Add the project root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load configuration
config = Config()
log_path = config.LOG_PATH
model_path = config.MODEL_PATH
data_path = config.DATA_PATH
model_info_path = config.MODEL_INFO_PATH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_arg_parser():
    """Set up command-line argument parser."""
    parser = argparse.ArgumentParser(description="DDoS Detection Tool")
    parser.add_argument('--sniff', action='store_true', help="Enable packet sniffing.")
    parser.add_argument('--preprocess', action='store_true', help="Enable data preprocessing.")
    parser.add_argument('--detect', action='store_true', help="Run threshold detection.")
    parser.add_argument('--train', action='store_true', help="Train machine learning model.")
    parser.add_argument('--predict', action='store_true', help="Predict anomalies using ML model.")
    parser.add_argument('--filter', action='store_true', help="Filter IPs based on anomalies.")
    parser.add_argument('--visualize', action='store_true', help="Generate anomaly visualization.")
    parser.add_argument('--packet_rate', type=int, help="Packet rate for threshold detection.")
    parser.add_argument('--src_ip', type=str, help="Source IP address for filtering.")
    return parser

def main():
    """Main entry point for the DDoS Detection Tool."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    logging.info("Configuration loaded successfully.")
    print("Configuration loaded successfully.")

    try:
        # Step 1: Packet Sniffing
        if args.sniff:
            print("Starting packet sniffing...")
            logging.info("Starting packet sniffing...")
            start_sniffing()

        # Step 2: Preprocessing
        if args.preprocess:
            print("Preprocessing data...")
            logging.info("Preprocessing data...")
            processed_data_path = preprocess_data(data_path)
            logging.info(f"Data preprocessed and saved to {processed_data_path}.")
        else:
            processed_data_path = data_path  # Use raw data if preprocessing is skipped

        # Step 3: Threshold Detection
        if args.detect:
            if args.packet_rate and args.src_ip:
                print(f"Running threshold detection for packet_rate={args.packet_rate}, src_ip={args.src_ip}...")
                logging.info("Running threshold detection...")
                threshold_detection(args.packet_rate, args.src_ip)
            else:
                logging.error("Threshold detection requires --packet_rate and --src_ip.")
                raise ValueError("Missing arguments for threshold detection.")

        # Step 4: Machine Learning - Training
        if args.train:
            print("Training machine learning model...")
            logging.info("Training ML model...")
            train_model(processed_data_path)
            logging.info("ML model trained successfully.")

        # Step 5: Machine Learning - Prediction
        if args.predict:
            print("Predicting anomalies...")
            logging.info("Predicting anomalies...")
            predict_anomaly(processed_data_path)
            logging.info("Anomaly prediction completed.")

        # Step 6: IP Filtering
        if args.filter:
            if args.src_ip:
                print(f"Filtering IP: {args.src_ip}...")
                logging.info("Filtering IP...")
                check_and_filter_ip(args.src_ip)
            else:
                logging.error("IP filtering requires --src_ip.")
                raise ValueError("Missing argument for IP filtering.")

        # Step 7: Visualization
        if args.visualize:
            print("Visualizing data...")
            logging.info("Generating visualization...")
            visualize_data(file_path=processed_data_path)
            logging.info("Visualization completed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

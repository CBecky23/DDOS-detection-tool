# src/main.py

import os
import sys
import logging
import argparse

# Add the project root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import Config
from src.utils.detection_log import log_detection
from src.capture.packet_sniffer import start_sniffing
from data.preprocess.preprocess import preprocess_data
from src.detection.threshold_detection import threshold_detection
from src.detection.ml_detection import train_model, predict_anomaly
from src.filtering.ip_filter import check_and_filter_ip
from src.visualize.visualize_data import visualize_data

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
    parser.add_argument('--file_path', type=str, help="Path to the CSV file for visualization.")
    parser.add_argument('--timestamp_col', type=str, default='timestamp', help="Column name for timestamps.")
    parser.add_argument('--value_col', type=str, default='value', help="Column name for values to plot.")
    parser.add_argument('--anomaly_col', type=str, default='anomaly', help="Column name for anomalies.")
    parser.add_argument('--plot_type', type=str, default='line', help="Type of plot ('line' or 'scatter').")
    return parser

def main():
    """Main entry point for the DDoS Detection Tool."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    # Load and validate configuration
    config = Config(config_file="../config/config.json")
    config.validate()

    logging.info("Configuration loaded successfully.")
    print("Configuration loaded successfully.")

    try:
        # Step 1: Packet Sniffing
        if args.sniff:
            print("Sniffing packets...")
            logging.info("Sniffing packets...")
            start_sniffing()

        # Step 2: Data Preprocessing
        if args.preprocess:
            print("Preprocessing data...")
            logging.info("Preprocessing data...")
            preprocess_data()

        # Step 3: Threshold Detection
        if args.detect:
            if args.packet_rate and args.src_ip:
                print(f"Running threshold detection for packet_rate={args.packet_rate}, src_ip={args.src_ip}...")
                logging.info("Running threshold detection...")
                threshold_detection(args.packet_rate, args.src_ip)
            else:
                logging.error("Threshold detection requires --packet_rate and --src_ip.")
                raise ValueError("Missing arguments for threshold detection.")

        # Step 4: Training Model
        if args.train:
            print("Training model...")
            logging.info("Training model...")
            train_model(config.PROCESSED_DATA_PATH)
            logging.info("Model training completed.")

        # Step 5: Predicting Anomalies
        if args.predict:
            print("Predicting anomalies...")
            logging.info("Predicting anomalies...")
            predict_anomaly()
            logging.info("Anomaly prediction completed.")

        # Step 6: Filtering IPs
        if args.filter:
            if args.src_ip:
                print(f"Filtering IPs for src_ip={args.src_ip}...")
                logging.info("Filtering IPs...")
                check_and_filter_ip(args.src_ip)
            else:
                logging.error("Filtering requires --src_ip.")
                raise ValueError("Missing argument for filtering.")

        # Step 7: Visualization
        if args.visualize:
            if args.file_path:
                print("Generating visualization...")
                logging.info("Generating visualization...")
                visualize_data(
                    file_path=args.file_path,
                    timestamp_col=args.timestamp_col,
                    value_col=args.value_col,
                    anomaly_col=args.anomaly_col,
                    plot_type=args.plot_type
                )
                logging.info("Visualization completed.")
            else:
                logging.error("Visualization requires --file_path.")
                raise ValueError("Missing argument for visualization.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

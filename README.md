
# DDoS Detection Tool

## Overview

The DDoS Detection Tool is a comprehensive solution designed to detect and mitigate Distributed Denial of Service (DDoS) attacks. The tool provides functionalities for packet sniffing, data preprocessing, threshold detection, machine learning-based anomaly detection, IP filtering, and data visualization.

## Features

- **Packet Sniffing**: Capture network packets for analysis.
- **Data Preprocessing**: Clean and prepare raw data for analysis.
- **Threshold Detection**: Detect anomalies based on predefined thresholds.
- **Machine Learning**: Train and use machine learning models to detect anomalies.
- **IP Filtering**: Filter out malicious IP addresses based on detected anomalies.
- **Data Visualization**: Visualize data and highlight anomalies.



## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/DDoS_Detection_Tool.git
   cd DDoS_Detection_Tool
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Ensure the configuration file is in place:**

   Create a `config.json` file in the `config` directory with the necessary settings. Here is an example:

   ```json
   {
       "RAW_DATA_PATH": "../data/raw/captured_traffic.csv",
       "PROCESSED_DATA_PATH": "../data/processed/processed_data.csv",
       "LOG_PATH": "../logs/detection.log",
       "THRESHOLD_PACKET_RATE": 100,
       "CONTAMINATION_RATE": 0.01,
       "MODEL_PATH": "../models/trained_model.pkl",
       "MODEL_INFO_PATH": "../models/model_info",
       "ENV": "development"
   }
   ```

## Usage

Run the main script with the desired options:

```sh
python 

main.py

 --sniff --preprocess --detect --train --predict --filter --visualize --packet_rate 100 --src_ip 192.168.1.1 --file_path 

anomaly_detected.csv


```

### Command-Line Arguments

- `--sniff`: Enable packet sniffing.
- `--preprocess`: Enable data preprocessing.
- `--detect`: Run threshold detection.
- `--train`: Train machine learning model.
- `--predict`: Predict anomalies using ML model.
- `--filter`: Filter IPs based on anomalies.
- `--visualize`: Generate anomaly visualization.
- `--packet_rate`: Packet rate for threshold detection.
- `--src_ip`: Source IP address for filtering.
- `--file_path`: Path to the CSV file for visualization.
- `--timestamp_col`: Column name for timestamps (default: 'timestamp').
- `--value_col`: Column name for values to plot (default: 'value').
- `--anomaly_col`: Column name for anomalies (default: 'anomaly').
- `--plot_type`: Type of plot ('line' or 'scatter', default: 'line').

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

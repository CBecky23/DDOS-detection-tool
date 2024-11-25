# src/filtering/ip_filter.py
from collections import defaultdict
from datetime import datetime
from src.utils.detection_log import log_detection

THRESHOLD_RATE = 100
blacklist = set()
ip_packet_counts = defaultdict(int)

def check_and_filter_ip(src_ip):
    """Check and filter IP addresses."""
    # Add your IP filtering logic here
    print(f"Filtering IP: {src_ip}")

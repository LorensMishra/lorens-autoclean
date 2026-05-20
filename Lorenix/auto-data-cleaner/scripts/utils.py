import os
import logging

def setup_logger(name="DataCleanerLogger", log_file="logs/cleaning.log"):
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

def ensure_directories():
    directories = [
        "data/raw",
        "data/cleaned",
        "reports",
        "logs",
        "assets"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

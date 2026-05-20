import pandas as pd
import os
from scripts.utils import setup_logger

logger = setup_logger("ValidatorLogger", "logs/validation.log")

def validate_file(file_path_or_buffer, filename):
    """Validates if the file format is supported and if it can be read."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in ['.csv', '.xlsx', '.xls']:
        logger.error(f"Unsupported file format for {filename}")
        raise ValueError(f"Unsupported file format: {ext}. Only CSV and Excel files are supported.")
        
    try:
        if ext == '.csv':
            # Just read a few rows to check for corruption
            df = pd.read_csv(file_path_or_buffer, nrows=5)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path_or_buffer, nrows=5)
            
        if df.empty:
            logger.warning(f"File {filename} is empty.")
            
        logger.info(f"Successfully validated {filename}")
        return True
    except Exception as e:
        logger.error(f"File corruption or read error in {filename}: {str(e)}")
        raise ValueError(f"Could not read the file. It might be corrupted or incorrectly formatted. Error: {str(e)}")

def load_data(file_path_or_buffer, filename):
    """Loads the data into a pandas DataFrame."""
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == '.csv':
            df = pd.read_csv(file_path_or_buffer)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path_or_buffer)
        logger.info(f"Loaded {len(df)} rows from {filename}")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {filename}: {str(e)}")
        raise

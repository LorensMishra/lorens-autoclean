import pandas as pd
import numpy as np
from scripts.utils import setup_logger

logger = setup_logger("DataCleanerLogger", "logs/cleaning.log")

class DataCleaner:
    def __init__(self, df):
        self.original_df = df.copy()
        self.df = df.copy()
        self.stats = {
            "initial_rows": len(df),
            "final_rows": 0,
            "duplicates_removed": 0,
            "missing_filled_numeric": 0,
            "missing_filled_categorical": 0,
            "outliers_detected": {},
            "empty_rows_removed": 0
        }

    def clean_all(self, duplicate_subset=None):
        logger.info("Starting automated data cleaning process...")
        self.remove_empty_rows()
        self.remove_duplicates(subset=duplicate_subset)
        self.standardize_text()
        self.convert_dates()
        self.handle_missing_values()
        self.detect_outliers()
        
        self.stats["final_rows"] = len(self.df)
        logger.info("Data cleaning completed.")
        return self.df, self.stats

    def remove_empty_rows(self):
        empty_mask = self.df.isna().all(axis=1)
        empty_rows = self.df[empty_mask].copy()
        
        initial_len = len(self.df)
        self.df.dropna(how='all', inplace=True)
        removed = initial_len - len(self.df)
        self.stats["empty_rows_removed"] = removed
        self.stats["empty_rows_data"] = empty_rows
        if removed > 0:
            logger.info(f"Removed {removed} fully empty rows.")

    def remove_duplicates(self, subset=None):
        duplicate_mask = self.df.duplicated(subset=subset, keep='first')
        duplicate_rows = self.df[duplicate_mask].copy()
        
        initial_len = len(self.df)
        self.df.drop_duplicates(subset=subset, inplace=True)
        removed = initial_len - len(self.df)
        self.stats["duplicates_removed"] = removed
        self.stats["duplicate_rows_data"] = duplicate_rows
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows.")

    def standardize_text(self):
        # Strip spaces and convert to title case for string columns
        for col in self.df.select_dtypes(include=['object', 'string']).columns:
            try:
                # Only string operations on items that are strings or can be safely cast
                self.df[col] = self.df[col].astype(str).str.strip().str.title()
                # If we casted NaNs to 'Nan' string, revert them back if possible
                self.df[col].replace({'Nan': np.nan, 'None': np.nan}, inplace=True)
            except Exception as e:
                logger.warning(f"Could not standardize text in column {col}: {e}")
        logger.info("Standardized text columns.")

    def convert_dates(self):
        # Attempt to find date columns and convert them
        for col in self.df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    logger.info(f"Converted column '{col}' to datetime.")
                except Exception as e:
                    logger.warning(f"Could not convert {col} to datetime: {e}")

    def handle_missing_values(self):
        # Numeric: fill with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            missing_count = self.df[col].isna().sum()
            if missing_count > 0:
                median_val = self.df[col].median()
                self.df[col] = self.df[col].fillna(median_val)
                self.stats["missing_filled_numeric"] += missing_count
                logger.info(f"Filled {missing_count} missing values in '{col}' with median {median_val}.")

        # Categorical: fill with mode
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            missing_count = self.df[col].isna().sum()
            if missing_count > 0:
                mode_series = self.df[col].mode()
                mode_val = mode_series[0] if not mode_series.empty else "Unknown"
                self.df[col] = self.df[col].fillna(mode_val)
                self.stats["missing_filled_categorical"] += missing_count
                logger.info(f"Filled {missing_count} missing values in '{col}' with mode '{mode_val}'.")

    def detect_outliers(self):
        # IQR method
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            if outliers > 0:
                self.stats["outliers_detected"][col] = int(outliers)
                logger.info(f"Detected {outliers} outliers in column '{col}'.")

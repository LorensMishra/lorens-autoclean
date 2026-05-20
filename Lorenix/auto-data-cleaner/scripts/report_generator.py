import os
import pandas as pd
from scripts.utils import setup_logger

logger = setup_logger("ReportLogger", "logs/report.log")

def generate_report(stats, report_dir="reports"):
    os.makedirs(report_dir, exist_ok=True)
    
    txt_path = os.path.join(report_dir, "cleaning_summary.txt")
    csv_path = os.path.join(report_dir, "cleaning_summary.csv")
    
    # Generate TXT
    try:
        with open(txt_path, 'w') as f:
            f.write("=== AI-Powered Data Cleaning Summary ===\n\n")
            f.write(f"Total rows before cleaning: {stats.get('initial_rows', 0)}\n")
            f.write(f"Total rows after cleaning: {stats.get('final_rows', 0)}\n")
            f.write(f"Fully empty rows removed: {stats.get('empty_rows_removed', 0)}\n")
            f.write(f"Duplicate rows removed: {stats.get('duplicates_removed', 0)}\n")
            f.write(f"Missing numeric values filled: {stats.get('missing_filled_numeric', 0)}\n")
            f.write(f"Missing categorical values filled: {stats.get('missing_filled_categorical', 0)}\n")
            
            f.write("\nOutliers Detected (IQR Method):\n")
            if stats.get('outliers_detected'):
                for col, count in stats['outliers_detected'].items():
                    f.write(f"  - {col}: {count} outliers\n")
            else:
                f.write("  None detected\n")
        logger.info(f"Saved text report to {txt_path}")
    except Exception as e:
        logger.error(f"Failed to generate txt report: {e}")

    # Generate CSV
    try:
        report_df = pd.DataFrame([
            {"Metric": "Total rows before cleaning", "Value": stats.get('initial_rows', 0)},
            {"Metric": "Total rows after cleaning", "Value": stats.get('final_rows', 0)},
            {"Metric": "Fully empty rows removed", "Value": stats.get('empty_rows_removed', 0)},
            {"Metric": "Duplicate rows removed", "Value": stats.get('duplicates_removed', 0)},
            {"Metric": "Missing numeric values filled", "Value": stats.get('missing_filled_numeric', 0)},
            {"Metric": "Missing categorical values filled", "Value": stats.get('missing_filled_categorical', 0)},
        ])
        
        outliers_df = pd.DataFrame([
            {"Metric": f"Outliers in {col}", "Value": count} 
            for col, count in stats.get('outliers_detected', {}).items()
        ])
        
        final_report_df = pd.concat([report_df, outliers_df], ignore_index=True)
        final_report_df.to_csv(csv_path, index=False)
        logger.info(f"Saved CSV report to {csv_path}")
    except Exception as e:
        logger.error(f"Failed to generate csv report: {e}")
        
    return txt_path, csv_path

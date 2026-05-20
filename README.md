# Lorenix AI-Powered Automated Data Cleaning System

<img width="1918" height="661" alt="1_FrontPage" src="https://github.com/user-attachments/assets/63143acf-ffba-4ca2-babe-9f2bc3d519c6" />

A complete professional Python-based automation system that automatically cleans messy CSV or Excel datasets, generates cleaned files, reports, and visual summaries.

## Features
- **File Upload**: Supports CSV and Excel via Drag-and-Drop.
 <img width="1918" height="661" alt="1_FrontPage" src="https://github.com/user-attachments/assets/2d9f635b-f639-4d51-9f08-b97414d3d9fe" />

- **Intelligent Cleaning**:
  - Removes duplicate rows
  - Strips extra spaces and standardizes text to Title Case
  - Standardizes categorical values
  - Detects and converts date columns
  - Fills missing numeric values with median
  - Fills missing categorical values with mode
  - Removes fully empty rows
  - Detects outliers using the IQR method
<img width="1914" height="880" alt="6_raw_and_cleaning_data_result" src="https://github.com/user-attachments/assets/093f8980-35b1-4226-9933-e5cdd821080e" />

- **Reporting**: Generates text and CSV summaries of the cleaning process.
- **Modern Dashboard**: Built with Streamlit, featuring a dark mode UI and Lorenix branding.
- **Visualizations**: View missing values and correlation heatmaps.

## Tech Stack
- Python
- Pandas & NumPy
- Streamlit
- Matplotlib & Seaborn

## Installation

1. Clone the repository or navigate to the project directory.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser to the URL provided (usually `http://localhost:8501`).
3. Upload your dataset (`sample_dataset.csv` is provided for testing).
4. Click "Run AI Cleaning" to process the data.
5. Preview the cleaned data and visualizations.
6. Download the cleaned file and generated reports from the sidebar.

## Folder Structure
```text
auto-data-cleaner/
├── assets/                  # Logos and images
├── data/
│   ├── cleaned/             # Output directory for clean data
│   └── raw/                 # Original data (if needed)
├── logs/                    # Application and cleaning logs
├── reports/                 # Auto-generated summaries
├── scripts/
│   ├── cleaner.py           # Core DataCleaner class
│   ├── report_generator.py  # Report creation logic
│   ├── utils.py             # Logging and directory management
│   └── validator.py         # File validation logic
├── app.py                   # Streamlit UI
├── requirements.txt         # Dependencies
├── README.md                # Documentation
└── sample_dataset.csv       # Test file
```

## Future Improvements
- Add database integration (SQLite/PostgreSQL)
- Add automated scheduled cleaning jobs
- Add AI-based cleaning suggestions via LLMs
- Batch file processing

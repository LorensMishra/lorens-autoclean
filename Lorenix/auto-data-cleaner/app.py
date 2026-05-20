import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

from scripts.utils import ensure_directories, setup_logger
from scripts.validator import validate_file, load_data
from scripts.cleaner import DataCleaner
from scripts.report_generator import generate_report

# Initialize directories and logger
ensure_directories()
logger = setup_logger("AppLogger", "logs/app.log")

# Setup page configuration
st.set_page_config(
    page_title="Lorenix - AI Data Cleaner",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Dark Mode and Lorenix Branding
def local_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0B0E14;
            color: #E0E0E0;
            font-family: 'Inter', sans-serif;
        }
        
        /* Sidebar styling */
        .css-1d391kg, [data-testid="stSidebar"] {
            background-color: #151821 !important;
            border-right: 1px solid #2A2D3A;
        }

        /* Header Banner with multiple backgrounds */
        .hero-banner {
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(98, 0, 234, 0.25) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(0, 229, 255, 0.25) 0%, transparent 50%),
                linear-gradient(135deg, #151821 0%, #0B0E14 100%);
            border-radius: 16px;
            padding: 20px 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.05);
            display: flex;
            align-items: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            flex-wrap: wrap;
        }
        .hero-content {
            margin-left: 20px;
            flex: 1;
            min-width: 250px;
        }

        /* Gradient Text */
        .gradient-text {
            background: linear-gradient(90deg, #00E5FF, #9D4EDD);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.2rem;
            margin-top: 0;
            margin-bottom: 5px;
            line-height: 1.2;
        }
        
        .sub-header {
            color: #B2C2D4;
            font-size: 1.1rem;
            margin-top: 0px;
            margin-bottom: 0;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #6200EA, #9D4EDD);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(98, 0, 234, 0.25);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(98, 0, 234, 0.4);
        }

        /* Cards and Dataframes */
        .stDataFrame {
            border: 1px solid #2A2D3A;
            border-radius: 10px;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .stDataFrame:hover {
            box-shadow: 0 8px 24px rgba(0,229,255,0.1);
            border-color: rgba(0,229,255,0.3);
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem;
            color: #00E5FF;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_base64 = get_image_base64("assets/logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="width: 75px; height: 75px; object-fit: cover; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,229,255,0.2);">' if logo_base64 else ''

header_html = f"""
<div class="hero-banner">
    <div class="hero-logo">
        {logo_html}
    </div>
    <div class="hero-content">
        <h1 class="gradient-text" style="margin-top:0;">Lorenix Data Cleaner</h1>
        <p class="sub-header">AI-Powered Automated Data Standardization and Cleansing</p>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

st.markdown("Upload your messy CSV or Excel datasets using the sidebar, and our intelligent system will automatically clean, standardize, and summarize your data.")
st.markdown("---")

# Sidebar
st.sidebar.header("📁 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Drag and drop file here", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    filename = uploaded_file.name
    logger.info(f"File uploaded: {filename}")
    
    try:
        if validate_file(uploaded_file, filename):
            uploaded_file.seek(0)
            df = load_data(uploaded_file, filename)
            
            st.subheader("Raw Data Preview")
            st.dataframe(df, use_container_width=True, height=300)
            
            st.sidebar.markdown("---")
            st.sidebar.header("⚙️ Cleaning Options")
            
            duplicate_cols = st.sidebar.multiselect(
                "Columns for Duplicate Removal (Leave empty for all)",
                options=df.columns.tolist()
            )
            
            run_clean = st.sidebar.button("Run AI Cleaning", use_container_width=True)
            
            if run_clean:
                with st.spinner("Analyzing and cleaning data..."):
                    cleaner = DataCleaner(df)
                    cleaned_df, stats = cleaner.clean_all(duplicate_subset=duplicate_cols if duplicate_cols else None)
                    
                    # Save cleaned data
                    cleaned_file_path = os.path.join("data/cleaned", f"cleaned_{filename}")
                    if filename.endswith('.csv'):
                        cleaned_df.to_csv(cleaned_file_path, index=False)
                    else:
                        cleaned_df.to_excel(cleaned_file_path, index=False)
                        
                    # Generate report
                    txt_report, csv_report = generate_report(stats)
                    
                    st.success("Data cleaning completed successfully!")
                    
                    preview_col1, preview_col2 = st.columns([3, 1])
                    with preview_col1:
                        st.subheader("Cleaned Data Preview")
                    with preview_col2:
                        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                        with open(cleaned_file_path, "rb") as file:
                            st.download_button(
                                label="⬇️ Save as CSV" if filename.endswith('.csv') else "⬇️ Save as Excel",
                                data=file,
                                file_name=f"cleaned_{filename}",
                                mime="text/csv" if filename.endswith('.csv') else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="main_download_cleaned"
                            )
                    
                    st.dataframe(cleaned_df, use_container_width=True, height=300)
                    
                    # Display Stats
                    st.subheader("📊 Cleaning Summary")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("🗑️ Rows Removed (Empty)", stats['empty_rows_removed'])
                    col2.metric("🔄 Duplicates Removed", stats['duplicates_removed'])
                    col3.metric("✨ Values Imputed", stats['missing_filled_numeric'] + stats['missing_filled_categorical'])
                    
                    # Display Removed Data
                    st.subheader("🗑️ Removed Data Details")
                    
                    with st.expander("View Removed Empty Rows"):
                        empty_data = stats.get('empty_rows_data')
                        if empty_data is not None and not empty_data.empty:
                            st.dataframe(empty_data, use_container_width=True)
                        else:
                            st.info("No fully empty rows were removed.")
                            
                    with st.expander("View Removed Duplicate Rows"):
                        duplicate_data = stats.get('duplicate_rows_data')
                        if duplicate_data is not None and not duplicate_data.empty:
                            st.dataframe(duplicate_data, use_container_width=True)
                        else:
                            st.info("No duplicate rows were removed.")
                            
                    # Visualizations
                    st.subheader("📈 Data Insights")
                    tab1, tab2 = st.tabs(["Missing Values", "Correlation Heatmap"])
                    
                    with tab1:
                        st.markdown("**Missing Values Before Cleaning**")
                        missing = df.isna().sum()
                        missing = missing[missing > 0]
                        if not missing.empty:
                            fig, ax = plt.subplots(figsize=(8, 4))
                            sns.barplot(x=missing.index, y=missing.values, palette="mako", ax=ax)
                            ax.set_ylabel("Count")
                            plt.xticks(rotation=45)
                            fig.patch.set_facecolor('#0E1117')
                            ax.set_facecolor('#0E1117')
                            ax.tick_params(colors='white')
                            ax.xaxis.label.set_color('white')
                            ax.yaxis.label.set_color('white')
                            st.pyplot(fig)
                        else:
                            st.info("No missing values in the original dataset.")
                            
                    with tab2:
                        st.markdown("**Correlation Heatmap (Cleaned Numeric Data)**")
                        numeric_df = cleaned_df.select_dtypes(include='number')
                        if len(numeric_df.columns) > 1:
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
                            fig.patch.set_facecolor('#0E1117')
                            ax.tick_params(colors='white')
                            st.pyplot(fig)
                        else:
                            st.info("Not enough numeric columns for a correlation heatmap.")
                            
                    # Downloads
                    st.sidebar.markdown("---")
                    st.sidebar.header("📥 Downloads")
                    
                    # Read back cleaned file
                    with open(cleaned_file_path, "rb") as file:
                        btn = st.sidebar.download_button(
                            label="⬇️ Download Cleaned Data",
                            data=file,
                            file_name=f"cleaned_{filename}",
                            mime="text/csv" if filename.endswith('.csv') else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                    with open(txt_report, "rb") as file:
                        st.sidebar.download_button(
                            label="📄 Download Summary Report (TXT)",
                            data=file,
                            file_name="cleaning_summary.txt",
                            mime="text/plain"
                        )

    except Exception as e:
        st.error(f"Error processing file: {e}")
        logger.error(f"Error processing {filename}: {e}")
else:
    st.info("Please upload a dataset from the sidebar to get started.")

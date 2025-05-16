import streamlit as st
import os
import time
import glob
import json
from datetime import datetime
from main import LongstockFlow

# Configure page and theme
st.set_page_config(
    page_title="Longstock",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styling
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    .main-header {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #1E3A8A !important;
        margin-bottom: 0 !important;
    }
    .subheader {
        font-size: 1.5rem !important;
        font-weight: 400 !important;
        color: #4B5563 !important;
        margin-top: 0 !important;
        margin-bottom: 2rem !important;
    }
    .section-header {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #1E3A8A !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid #E5E7EB !important;
    }
    .stButton>button {
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 0.5rem 2rem !important;
        border-radius: 0.5rem !important;
    }
    .stButton>button:hover {
        background-color: #2563EB !important;
    }
    .stSpinner>div {
        border-top-color: #1E3A8A !important;
    }
    .task-output {
        margin-bottom: 20px;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #1E3A8A;
        background-color: #f8f9fa;
    }
    .task-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 10px;
    }
    .task-time {
        font-size: 0.8rem;
        color: #6c757d;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for multi-page functionality
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'company_name' not in st.session_state:
    st.session_state.company_name = ''
if 'time_period' not in st.session_state:
    st.session_state.time_period = '1y'
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = 'medium'
if 'fundamental_completed' not in st.session_state:
    st.session_state.fundamental_completed = False
if 'technical_completed' not in st.session_state:
    st.session_state.technical_completed = False

def start_analysis():
    st.session_state.page = 'analysis'
    st.rerun()
    
def show_input_page():
    st.markdown('<h1 class="main-header">Longstock</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">AI-Powered Stock Analysis Platform</p>', unsafe_allow_html=True)
    
    # Create columns for a cleaner layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Enter Stock Details")
        with st.form("input_form"):
            st.session_state.company_name = st.text_input("Company Name", st.session_state.company_name, 
                                                          placeholder="e.g., Apple, Tesla, Microsoft")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.time_period = st.selectbox(
                    "Time Period", 
                    options=['1m', '3m', '6m', '1y', '2y', '5y', '10y'],
                    index=['1m', '3m', '6m', '1y', '2y', '5y', '10y'].index(st.session_state.time_period)
                )
            with col_b:
                st.session_state.risk_level = st.selectbox(
                    "Risk Level", 
                    options=['low', 'medium', 'high'],
                    index=['low', 'medium', 'high'].index(st.session_state.risk_level)
                )
            
            st.markdown("")  # Add some spacing
            submit = st.form_submit_button("Start Analysis")
            if submit:
                if st.session_state.company_name:
                    start_analysis()
                else:
                    st.error("Please enter a company name")
    
    with col2:
        st.markdown("### How It Works")
        st.markdown("""
        Longstock uses AI to analyze stocks based on:
        
        1. **Fundamental Analysis** - Evaluates company financials and business model
        
        2. **Technical Analysis** - Analyzes price charts and market trends
        
        The analysis is tailored to your specified risk level and time horizon.
        """)

def get_task_outputs(company_name):
    """Get all task output files for a company"""
    company_dir = f"outputs/{company_name}"
    task_files = []
    
    if os.path.exists(company_dir):
        file_paths = glob.glob(f"{company_dir}/*.md")
        for file_path in file_paths:
            task_name = os.path.basename(file_path).replace('.md', '')
            file_time = os.path.getmtime(file_path)
            task_files.append({
                "path": file_path,
                "task_name": task_name,
                "time": file_time
            })
    
    # Sort files by modification time (newest first)
    return sorted(task_files, key=lambda x: x["time"], reverse=True)

def display_task_outputs(company_name):
    """Display all task output files for a company"""
    task_files = get_task_outputs(company_name)
    
    if not task_files:
        st.info("No task outputs found for this analysis yet.")
        return
    
    for file_info in task_files:
        file_path = file_info["path"]
        task_name = file_info["task_name"]
        file_time = datetime.fromtimestamp(file_info["time"]).strftime("%Y-%m-%d %H:%M:%S")
        
        display_name = task_name.replace('_', ' ').title()
        
        # Display in a nice formatted container
        st.markdown(f"""
        <div class="task-output">
            <div class="task-title">{display_name}</div>
            <div class="task-time">Generated at: {file_time}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Output", expanded=False):
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    st.markdown(content)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

def run_analysis():
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Initialize flow
    flow = LongstockFlow()
    flow.state.company_name = st.session_state.company_name
    flow.state.time_period = st.session_state.time_period
    flow.state.risk_level = st.session_state.risk_level
    
    # Run fundamental analysis if not already completed
    if not st.session_state.fundamental_completed:
        # Run fundamental analysis
        progress_text = "Generating fundamental analysis. This may take a few minutes..."
        
        with st.spinner(progress_text):
            # Run the analysis
            flow.generate_fundamental_analysis()
            flow.save_fundamental_analysis()
            st.session_state.fundamental_completed = True
    
    # Show fundamental analysis results
    st.markdown('<h2 class="section-header">Fundamental Analysis</h2>', unsafe_allow_html=True)
    
    # Check for fundamental analysis file
    fundamental_file = f"output/{st.session_state.company_name}_fundamental_analysis.md"
    if os.path.exists(fundamental_file):
        with open(fundamental_file, "r") as f:
            st.markdown(f.read())
    
    # Display task outputs after fundamental analysis
    st.markdown("### Detailed Analysis By Task")
    display_task_outputs(st.session_state.company_name)
    
    # Run technical analysis if requested
    if st.session_state.fundamental_completed and not st.session_state.technical_completed:
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Continue to Technical Analysis"):
                progress_text = "Generating technical analysis. This may take a few minutes..."
                with st.spinner(progress_text):
                    # Run the analysis
                    flow.generate_technical_analysis()
                    flow.save_technical_analysis()
                    st.session_state.technical_completed = True
                    st.rerun()
    
    # Show technical analysis results
    if st.session_state.technical_completed:
        st.markdown('<h2 class="section-header">Technical Analysis</h2>', unsafe_allow_html=True)
        
        technical_file = f"output/{st.session_state.company_name}_technical_analysis.md"
        if os.path.exists(technical_file):
            # Show chart if available
            if flow.state.chart_path and os.path.exists(flow.state.chart_path):
                st.image(flow.state.chart_path, caption=f"{st.session_state.company_name} Price Chart")
                
            with open(technical_file, "r") as f:
                st.markdown(f.read())
        
        # Display updated task outputs after technical analysis
        st.markdown("### Detailed Analysis By Task")
        display_task_outputs(st.session_state.company_name)
    
    st.markdown("---")
    if st.button("Start New Analysis"):
        st.session_state.page = 'input'
        st.session_state.fundamental_completed = False
        st.session_state.technical_completed = False
        st.rerun()

# Main app logic
if st.session_state.page == 'input':
    show_input_page()
elif st.session_state.page == 'analysis':
    st.markdown(f'<h1 class="main-header">Longstock Analysis</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subheader">Analysis for {st.session_state.company_name} | {st.session_state.time_period} | Risk Level: {st.session_state.risk_level.capitalize()}</p>', unsafe_allow_html=True)
    run_analysis()

if __name__ == "__main__":
    pass 
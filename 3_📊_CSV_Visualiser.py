import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai
import plotly.express as px
import tempfile
from tabulate import tabulate

def create_gemini_agent(df):
    model = genai.GenerativeModel('gemini-pro')
    
    def analyze_dataframe(question):
        context = f"""
        You are analyzing a DataFrame with the following structure:
        Columns: {', '.join(df.columns)}
        Data Sample: 
        {df.head().to_markdown()}
        
        Statistical Summary:
        {df.describe().to_markdown()}
        
        Question: {question}
        """
        response = model.generate_content(context)
        return response.text

    return analyze_dataframe

def main():
    st.title("📊 Excel Data Analyzer")
    
    # Load environment variables
    load_dotenv()
    
    # Configure Google API
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("GOOGLE_API_KEY is not set")
        st.stop()
    
    genai.configure(api_key=google_api_key)
    
    # Initialize session state
    if 'question_history' not in st.session_state:
        st.session_state.question_history = []

    csv_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if csv_file is not None:
        try:
            # Read CSV and create agent
            df = pd.read_csv(csv_file)
            agent = create_gemini_agent(df)
            
            # Data Overview
            with st.expander("📈 Data Overview"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", df.shape[0])
                with col2:
                    st.metric("Columns", df.shape[1])
                with col3:
                    st.metric("Missing Values", df.isna().sum().sum())
                
                st.dataframe(df.head())
                
            # Quick Visualizations
            with st.expander("🎨 Quick Visualizations"):
                viz_col = st.selectbox("Select column to visualize:", df.columns)
                if df[viz_col].dtype in ['int64', 'float64']:
                    fig = px.histogram(df, x=viz_col)
                    st.plotly_chart(fig)
                else:
                    fig = px.bar(df[viz_col].value_counts())
                    st.plotly_chart(fig)
            
            # Sample Questions
            with st.expander("💡 Sample Questions"):
                st.markdown("""
                - What are the basic statistics for this dataset?
                - Are there any notable patterns in the data?
                - What are the key insights from this dataset?
                - Can you identify any outliers?
                """)
            
            # Question Input with History
            user_question = st.text_input("Ask a question about your CSV: ")
            
            if user_question:
                with st.spinner(text="Analyzing..."):
                    response = agent(user_question)
                    st.write(response)
                    # Add to history
                    st.session_state.question_history.append({
                        "question": user_question,
                        "answer": response
                    })
            
            # Display Question History
            if st.session_state.question_history:
                with st.expander("📝 Question History"):
                    for idx, qa in enumerate(st.session_state.question_history):
                        st.markdown(f"**Q{idx+1}: {qa['question']}**")
                        st.markdown(f"A: {qa['answer']}")
                        st.markdown("---")
            
            # Export Options
            with st.expander("📥 Export Options"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Export Analysis Report"):
                        report = "\n\n".join([
                            f"Q: {qa['question']}\nA: {qa['answer']}"
                            for qa in st.session_state.question_history
                        ])
                        st.download_button(
                            "Download Report",
                            report,
                            file_name="analysis_report.txt"
                        )
                with col2:
                    if st.button("Export Processed Data"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "Download CSV",
                            csv,
                            file_name="processed_data.csv"
                        )
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

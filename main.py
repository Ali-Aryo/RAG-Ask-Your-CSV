import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pandas as pd
import io
import re


def clean_csv(uploaded_file):
    """Clean CSV by removing metadata and fixing formatting issues"""
    try:
        # Read the raw content
        content = uploaded_file.getvalue().decode('utf-8')
        lines = content.split('\n')
        
        # Find the actual header line (should contain "Geography" and other column names)
        header_idx = -1
        for i, line in enumerate(lines):
            if 'Geography' in line and 'Trade flow detail' in line:
                header_idx = i
                break
        
        if header_idx == -1:
            # Fallback: look for line with multiple commas
            for i, line in enumerate(lines):
                if line.count(',') > 3:
                    header_idx = i
                    break
        
        if header_idx == -1:
            # If still not found, use original file
            return uploaded_file
        
        # Get header and data lines
        header_line = lines[header_idx]
        data_lines = lines[header_idx + 1:]
        
        # Filter out empty lines and lines that don't match the column structure
        num_columns = header_line.count(',') + 1
        clean_data_lines = []
        
        for line in data_lines:
            line = line.strip()
            if line and not line.startswith(('Symbol legend', 'Footnotes:', 'How to cite:', 'https:')):
                # Check if line has roughly the right number of columns (allow some flexibility)
                line_columns = line.count(',') + 1
                if line_columns >= num_columns - 2:  # Allow some flexibility
                    clean_data_lines.append(line)
        
        # Combine header and clean data
        clean_lines = [header_line] + clean_data_lines
        
        # Join back into string and convert to file-like object
        clean_content = '\n'.join(clean_lines)
        return io.StringIO(clean_content)
    
    except Exception as e:
        st.error(f"Error cleaning CSV: {str(e)}")
        return uploaded_file

def main(): 

    load_dotenv()

    st.set_page_config(page_title="RAG-Ask-Your-CSV", page_icon=":books:")
    st.header("RAG-Ask-Your-CSV")

    user_csv = st.file_uploader("Upload your CSV file", type=["csv"])

    if user_csv is not None:

        user_csv = clean_csv(user_csv)

        user_question = st.text_input("Ask a question about your data?:")

        llm = ChatOpenAI(
            temperature=0,
            model= "gpt-4.1-mini",
            max_tokens=10000,
        )

        agent = create_csv_agent(llm, user_csv, verbose=True, allow_dangerous_code=True)

        if user_question is not None and user_question != "":
            response = agent.run(user_question)
            st.write(response)

if __name__ == "__main__":
    main()      
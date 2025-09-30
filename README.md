# RAG-Ask-Your-CSV

A Streamlit web application that allows you to analyze CSV data using natural language queries powered by OpenAI's GPT models and LangChain.

## Features

- Upload CSV files with automatic metadata cleaning
- Ask questions about your data in natural language
- Powered by OpenAI GPT-4o-mini for intelligent data analysis
- Handles messy CSV files

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up OpenAI API Key

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

### 3. Run the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. Upload a CSV file using the file uploader
2. Type your question about the data in natural language
3. Get intelligent analysis and insights from your data

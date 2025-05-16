# Longstock: AI-Powered Stock Analysis Platform

Longstock is a Streamlit-based web application that provides AI-powered stock analysis using two major components:

1. **Fundamental Analysis** - Evaluates company financials, business model, and growth prospects
2. **Technical Analysis** - Analyzes price charts, trends, and patterns

## Features

- User-friendly interface for entering company details
- Customizable time period and risk profile
- Detailed fundamental analysis reports
- Technical analysis with visual charts
- Step-by-step workflow

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/longstock.git
cd longstock

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:

```bash
streamlit run app.py
```

2. Access the application in your browser (typically at http://localhost:8501)

3. Enter a company name, select time period and risk level

4. Review the fundamental analysis

5. Proceed to technical analysis

6. Start a new analysis if desired

## Project Structure

- `app.py` - Streamlit application frontend
- `main.py` - CrewAI flow implementation
- `crews/` - AI crews for different analysis types
  - `fundamental_crew/` - AI crew for fundamental analysis
  - `technical_crew/` - AI crew for technical analysis
- `financial_data.py` - Financial data retrieval functions
- `output/` - Generated analysis reports

## Requirements

- Python 3.8+
- Streamlit
- CrewAI
- YFinance
- Pandas
- AgentOps

## License

MIT


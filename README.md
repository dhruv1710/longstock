# LongStock

LongStock is an AI-powered fundamental and technical analysis tool for stock evaluation using CrewAI. It leverages a team of specialized AI agents to analyze financial data and provide comprehensive investment insights.

## Overview

LongStock uses a flow-based approach where different AI agents' crews work together to analyze various aspects of a company's financial data and market position. Each agent specializes in a different area of fundamental analysis:

1. **Financial Data Collector** - Gathers comprehensive financial data for analysis
2. **Financial Statement Analyst** - Analyzes balance sheets, income statements, and cash flow statements
3. **Valuation Expert** - Calculates and interprets valuation metrics
4. **Growth Analyst** - Evaluates historical growth patterns and future potential
5. **Competitive Advantage Assessor** - Identifies competitive moats and market positioning
6. **Capital Allocation Analyst** - Evaluates how effectively management allocates capital
7. **Fundamental Synthesis Agent** - Integrates findings into a comprehensive assessment

## Requirements

- Python 3.12+
- Dependencies as listed in pyproject.toml:
  - crewai[tools] >= 0.119.0
  - ruff >= 0.11.9
- Additional dependencies:
  - yfinance
  - pandas

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd longstock

# Create and activate virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Usage

To run a fundamental analysis:

```bash
python main.py
```

The application will prompt you for:
- Company name
- Time period for analysis (e.g., 5y)
- Risk level (low, medium, high)

The output will be saved to a file named `fundamental_analysis.txt`.

## Project Structure

```
longstock/
├── crews/
│   ├── fundamental_crew/     # Fundamental analysis crew
│   │   ├── config/
│   │   │   ├── agents.yaml   # Agent configurations
│   │   │   └── tasks.yaml    # Task definitions
│   │   └── fundamental_crew.py
│   └── poem_crew/            # Secondary crew
├── tools/                    # Custom tools
│   └── custom_tool.py        # Example custom tool
├── main.py                   # Application entry point
├── pyproject.toml            # Project dependencies
└── README.md                 # This file
```

## How It Works

1. The system collects user input for the company to analyze
2. The FundamentalCrew is initialized with specialized AI agents
3. Each agent performs specific analysis tasks:
   - Collecting financial data
   - Analyzing financial statements
   - Calculating valuation metrics
   - Assessing growth potential
   - Evaluating competitive position
   - Analyzing capital allocation
   - Synthesizing overall findings
4. The results are compiled into a comprehensive fundamental analysis report

## Extending the System

To add new capabilities:
- Add new agents to the crew by extending the FundamentalCrew class
- Create custom tools in the tools directory
- Configure agent behaviors and task definitions in the YAML configuration files


#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crews.fundamental_crew.fundamental_crew import FundamentalCrew
from crews.technical_crew.technical_crew import TechnicalCrew
from financial_data import get_financial_data, chart_tool, get_ticker
import pandas as pd
import yfinance as yf
import agentops
import os

class LongstockState(BaseModel):
    company_name: str = ""
    time_period: str = ""
    risk_level: str = ""
    fundamental_analysis: str = ""
    technical_analysis: str = ""
    finance_data: str = ""
    chart_path: str = ""
    

class LongstockFlow(Flow[LongstockState]):

    @start()
    def get_user_input(self):
        # This method is kept for CLI usage but can be bypassed in Streamlit
        # by directly setting state variables
        print("\n=== Company ===\n")
        self.state.company_name = input("Enter company name: ")
        print("\n=== Time Period ===\n")
        self.state.time_period = input("Enter time period (e.g., 5y): ")
        print("\n=== Risk Level ===\n")
        self.state.risk_level = input("Enter risk level (low, medium, high): ")
        
    @listen(get_user_input)
    def generate_fundamental_analysis(self):
        print("Working on fundamental analysis")
        self.state.finance_data = get_financial_data(self.state.company_name, 3)
        ticker = get_ticker(self.state.company_name)
        result = (
            FundamentalCrew()
            .crew()
            .kickoff(inputs={"company_name": self.state.company_name, "time_period": self.state.time_period, "risk_level": self.state.risk_level, "ticker": ticker, "financial_data": self.state.finance_data})
        )

        print("Fundamental analysis generated")
        self.state.fundamental_analysis = result.raw

    @listen(generate_fundamental_analysis)
    def save_fundamental_analysis(self):
        print("Saving fundamental analysis")
        os.makedirs("outputs", exist_ok=True)
        with open(f"outputs/{self.state.company_name}/fundamental_analysis.md", "w") as f:
            print(self.state.fundamental_analysis)
            f.write(self.state.fundamental_analysis)

    @listen(save_fundamental_analysis)
    def generate_technical_analysis(self):
        print("Working on technical analysis")
        self.state.chart_path = chart_tool(self.state.company_name)
        ticker = get_ticker(self.state.company_name)
        result = (
            TechnicalCrew()
            .crew()
            .kickoff(inputs={"company_name": self.state.company_name, "time_period": self.state.time_period, "risk_level": self.state.risk_level, "ticker": ticker, "chart_file": self.state.chart_path})
        )

        print("Technical analysis generated")
        self.state.technical_analysis = result.raw

    @listen(generate_technical_analysis)
    def save_technical_analysis(self):
        print("Saving technical analysis")
        os.makedirs("outputs", exist_ok=True)
        with open(f"outputs/{self.state.company_name}/technical_analysis.md", "w") as f:
            print(self.state.technical_analysis)
            f.write(self.state.technical_analysis)

def kickoff():
    longstock_flow = LongstockFlow()
    longstock_flow.kickoff()


def plot():
    longstock_flow = LongstockFlow()
    longstock_flow.plot()


if __name__ == "__main__":

    agentops.init(
    api_key=os.getenv("AGENTOPS_API_KEY"),
    default_tags=['crewai']
)
    # kickoff()
    LongstockFlow().plot()


    # output = FundamentalCrew().crew().kickoff(inputs={"company_name": 'TCS', "time_period": '2y', "risk_level": 'high', "ticker_symbol":"TCS"})
    # print(output.raw)

    # output = TechnicalCrew().crew().kickoff(inputs={"company_name": 'TCS', "time_period": '2y', "risk_level": 'high', "ticker_symbol":"TCS"})
    # print(output.raw)
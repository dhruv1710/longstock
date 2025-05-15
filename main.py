#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crews.fundamental_crew.fundamental_crew import FundamentalCrew
from financial_data import get_financial_data
import pandas as pd
import yfinance as yf

class LongstockState(BaseModel):
    company_name: str = ""
    time_period: str = ""
    risk_level: str = ""
    fundamental_analysis: str = ""
    finance_data: str = ""
    

class LongstockFlow(Flow[LongstockState]):

    @start()
    def get_user_input(self):
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
        result = (
            FundamentalCrew()
            .crew()
            .kickoff(inputs={"company_name": self.state.company_name, "time_period": self.state.time_period, "risk_level": self.state.risk_level, "ticker":"TCS", "financial_data": self.state.finance_data})
        )

        print("Poem generated", result.raw)
        self.state.fundamental_analysis = result.raw

    @listen(generate_fundamental_analysis)
    def save_fundamental_analysis(self):
        print("Saving poem")
        with open("fundamental_analysis.txt", "w") as f:
            print(self.state.fundamental_analysis)
            f.write(self.state.fundamental_analysis)


def kickoff():
    longstock_flow = LongstockFlow()
    longstock_flow.kickoff()


def plot():
    longstock_flow = LongstockFlow()
    longstock_flow.plot()


if __name__ == "__main__":
    kickoff()


    # output = FundamentalCrew().crew().kickoff(inputs={"company_name": 'TCS', "time_period": '2y', "risk_level": 'high', "ticker_symbol":"TCS"})
    # print(output.raw)
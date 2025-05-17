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
from crewai import Agent, Task, Crew, Process
import os
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

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

    @listen(save_technical_analysis)
    def generate_sentiment_analysis(self):
        print("Working on sentiment analysis")
        ticker = get_ticker(self.state.company_name)

        sentiment_agent = Agent(
            role="Sentiment Analyst",
            goal="Analyze recent Yahoo Finance news and articles to evaluate the sentiment of public and media perception around a given stock ticker.",
            backstory="You are a specialized financial sentiment expert. Your job is to assess recent news and signals from Yahoo Finance and classify the prevailing market sentiment—bullish, bearish, or neutral. You use a combination of NLP tools and financial heuristics to determine how the stock is being perceived, which helps traders and analysts act on soft signals early.",
            llm='gemini/gemini-2.5-flash-preview-04-17',
            tools=[YahooFinanceNewsTool()]
        )

        sentiment_task = Task(
            description='''
Analyze the sentiment of recent news about {ticker} using Yahoo Finance headlines and summaries.
    
    Focus on:
    1. Number of positive, negative, and neutral news stories
    2. General media tone — optimistic, cautious, panicked, etc.
    3. Repeated themes (e.g. layoffs, strong earnings, product delays)

    Return a sentiment summary (bullish, bearish, neutral) with reasoning.''',
            expected_output='''A structured summary of sentiment across recent news articles about the company,
    including categorized news counts (positive/negative/neutral), dominant themes,
    and an overall sentiment rating with a brief rationale.''',
            agent=sentiment_agent,
            output_file=f'outputs/{self.state.company_name}/sentiment_analysis.md',
            create_directory=True
        )
        sentiment_crew = Crew(
            agents=[sentiment_agent],
            tasks=[sentiment_task],
            process=Process.sequential,
            verbose=True,
        )
        sentiment_crew.kickoff(inputs={"company_name": self.state.company_name, "ticker": ticker})
    

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
    kickoff()


    # output = FundamentalCrew().crew().kickoff(inputs={"company_name": 'TCS', "time_period": '2y', "risk_level": 'high', "ticker_symbol":"TCS"})
    # print(output.raw)

    # output = TechnicalCrew().crew().kickoff(inputs={"company_name": 'TCS', "time_period": '2y', "risk_level": 'high', "ticker_symbol":"TCS"})
    # print(output.raw)
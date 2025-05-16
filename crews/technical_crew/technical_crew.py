from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from financial_data import get_ticker
from crewai.tools import tool
import yfinance as yf
# import pandas_ta as ta
import matplotlib.pyplot as plt



from tools.yfinance_tool import YFinanceTool
from crewai_tools import SerperDevTool




@CrewBase
class TechnicalCrew():
    """TechnicalCrew crew"""
    
    

    agents: List[BaseAgent]
    tasks: List[Task]
    
    
    @agent
    def chart_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['chart_analyzer'],
            verbose=True,
            model=True
        )

    @agent
    def technical_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_strategy_agent'],
            verbose=True
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'],
            verbose=True
        )
    
    
    
    @task
    def analyze_chart_task(self) -> Task:
        
        return Task(
            config=self.tasks_config['analyze_chart_task'],
            output_file=f'outputs/chart_analysis.md',
            create_directory=True
        )

    @task
    def generate_trade_signal_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_trade_signal_task'],
            output_file=f'outputs/trade_signal.md',
            create_directory=True
        )

    @task
    def generate_technical_analysis_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_technical_analysis_report_task'],
        )

    @crew
    def crew(self, ) -> Crew:
        """Creates the TechnicalCrew crew"""
        
        

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            output_log_file='outputlogs.txt'
        )

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List





@CrewBase
class FundamentalCrew():
    """FundamentalCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    
    
    @agent
    def financial_statement_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_statement_analyst'], 
            verbose=True
        )

    @agent
    def valuation_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['valuation_expert'], 
            verbose=True
        )

    @agent
    def growth_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['growth_analyst'], 
            verbose=True
        )

    @agent
    def competitive_advantage_assessor(self) -> Agent:
        return Agent(
            config=self.agents_config['competitive_advantage_assessor'], 
            verbose=True
        )

    @agent
    def capital_allocation_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['capital_allocation_analyst'], 
            verbose=True
        )

    @agent
    def fundamental_synthesis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['fundamental_synthesis_agent'], 
            verbose=True
        )

    
    
    
    @task
    def collect_financial_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['collect_financial_data_task'], 
        )
    
    @task
    def analyze_financial_statements_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_financial_statements_task'], 
        )

    @task
    def calculate_valuation_metrics_task(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_valuation_metrics_task'], 
            output_file='report.md'
        )

    @task
    def assess_growth_potential_task(self) -> Task:
        return Task(
            config=self.tasks_config['assess_growth_potential_task'], 
        )

    @task
    def evaluate_competitive_position_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_competitive_position_task'], 
        )

    @task
    def analyze_capital_allocation_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_capital_allocation_task'], 
        )

    @task
    def synthesize_fundamentals_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesize_fundamentals_task'], 
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FundamentalCrew crew"""
        
        

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            
        )

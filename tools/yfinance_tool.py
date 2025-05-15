from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from financial_data import get_financial_data


class YFinanceToolInput(BaseModel):
    """Input schema for YFinanceTool."""

    ticker: str = Field(..., description="Ticker symbol of the company")


class YFinanceTool(BaseTool):
    name: str = "Yahoo Finance Tool"
    description: str = (
        "Use this tool to get the financial data of a company from Yahoo Finance using its ticker symbol"
    )
    args_schema: Type[BaseModel] = YFinanceToolInput

    def _run(self, ticker: str) -> str:
        return get_financial_data(ticker, 3)

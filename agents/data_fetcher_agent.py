"""
Data Fetcher Agent - Retrieves market data and financial metrics
Uses Claude Haiku for fast, efficient data operations
"""

from crewai import Agent
from config import ModelConfig
from llm_factory import LLMFactory
from tools.stock_data_tool import (
    get_stock_price,
    get_historical_prices,
    get_stock_fundamentals,
    get_multiple_stocks,
    calculate_portfolio_value,
)
import os


def create_data_fetcher_agent() -> Agent:
    """
    Create a Data Fetcher Agent specialized in retrieving stock data.

    This agent uses the configured LLM for simple data retrieval tasks.
    """
    # Get model name with provider prefix for CrewAI/LiteLLM
    model_name = LLMFactory.get_model_name("fetcher")

    return Agent(
        role="Market Data Fetcher",
        goal="Efficiently retrieve accurate stock market data, prices, and financial metrics",
        backstory="""You are a highly efficient data specialist with direct access to
        financial market data. Your primary responsibility is to quickly and accurately
        fetch stock prices, historical data, fundamentals, and portfolio values.

        You excel at:
        - Retrieving real-time stock prices
        - Gathering historical OHLCV data
        - Fetching company fundamentals (P/E, EPS, etc.)
        - Calculating portfolio values and compositions

        You always provide clean, structured data with proper error handling.
        When data is unavailable, you clearly communicate this and suggest alternatives.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,  # Pass model name as string for CrewAI
        tools=[
            get_stock_price,
            get_historical_prices,
            get_stock_fundamentals,
            get_multiple_stocks,
            calculate_portfolio_value,
        ],
    )


def create_data_fetcher_agent_with_custom_tools(additional_tools: list = None) -> Agent:
    """
    Create a Data Fetcher Agent with additional custom tools.

    Args:
        additional_tools: List of additional CrewAI tools to include
    """
    model_name = LLMFactory.get_model_name("fetcher")

    base_tools = [
        get_stock_price,
        get_historical_prices,
        get_stock_fundamentals,
        get_multiple_stocks,
        calculate_portfolio_value,
    ]

    if additional_tools:
        base_tools.extend(additional_tools)

    return Agent(
        role="Market Data Fetcher",
        goal="Efficiently retrieve accurate stock market data, prices, and financial metrics",
        backstory="""You are a highly efficient data specialist with direct access to
        financial market data. Your primary responsibility is to quickly and accurately
        fetch stock prices, historical data, fundamentals, and portfolio values.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,
        tools=base_tools,
    )


# Export
__all__ = ["create_data_fetcher_agent", "create_data_fetcher_agent_with_custom_tools"]

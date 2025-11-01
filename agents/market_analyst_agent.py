"""
Market Analyst Agent - Technical analysis and trend identification
Uses Claude Sonnet for balanced analytical capabilities
"""

from crewai import Agent
from config import ModelConfig
from llm_factory import LLMFactory
from tools.technical_indicators_tool import (
    calculate_indicators,
    analyze_momentum,
    detect_support_resistance,
)
from tools.stock_data_tool import get_historical_prices


def create_market_analyst_agent() -> Agent:
    """
    Create a Market Analyst Agent specialized in technical analysis.

    This agent uses the configured LLM for analytical reasoning.
    """
    model_name = LLMFactory.get_model_name("analyst")

    return Agent(
        role="Technical Market Analyst",
        goal="Analyze stock performance, identify trends, and provide technical insights",
        backstory="""You are an expert technical analyst with 20 years of experience
        in equity markets. You specialize in identifying trends, chart patterns,
        support/resistance levels, and technical indicators.

        Your expertise includes:
        - Technical indicator analysis (RSI, MACD, Moving Averages, Bollinger Bands)
        - Trend identification (uptrends, downtrends, consolidation)
        - Support and resistance level detection
        - Momentum analysis
        - Volume analysis
        - Chart pattern recognition

        You provide clear, actionable insights based on technical analysis.
        You always consider multiple timeframes and confirm signals across indicators.
        When trends are unclear, you clearly state this and provide context.

        Your analysis is data-driven and objective, avoiding emotional bias.
        You present both bullish and bearish scenarios when appropriate.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,
        tools=[
            calculate_indicators,
            analyze_momentum,
            detect_support_resistance,
            get_historical_prices,
        ],
    )


def create_market_analyst_agent_custom() -> Agent:
    """
    Create a Market Analyst Agent with custom configuration.
    """
    model_name = LLMFactory.get_model_name("analyst")

    return Agent(
        role="Technical Market Analyst",
        goal="Perform comprehensive technical analysis to identify trading opportunities and risks",
        backstory="""You are a seasoned technical analyst specializing in quantitative
        market analysis. You combine multiple technical indicators to form a complete
        picture of market conditions.

        Your approach:
        1. Gather historical price data
        2. Calculate key technical indicators
        3. Identify trends and momentum
        4. Detect support/resistance levels
        5. Synthesize findings into actionable insights

        You are known for your accuracy and ability to spot trend reversals early.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,
        tools=[
            calculate_indicators,
            analyze_momentum,
            detect_support_resistance,
            get_historical_prices,
        ],
        max_iter=15,  # Allow more iterations for thorough analysis
    )


# Export
__all__ = ["create_market_analyst_agent", "create_market_analyst_agent_custom"]

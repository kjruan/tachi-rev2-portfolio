"""
News Sentiment Agent - Analyzes market sentiment from news sources
Uses Claude Sonnet for excellent NLP and sentiment analysis
"""

from crewai import Agent
from config import ModelConfig
from llm_factory import LLMFactory
from tools.news_sentiment_tool import (
    get_recent_news,
    analyze_market_sentiment,
    get_analyst_ratings,
)


def create_sentiment_agent() -> Agent:
    """
    Create a News Sentiment Agent specialized in sentiment analysis.

    This agent uses the configured LLM for NLP capabilities.
    """
    model_name = LLMFactory.get_model_name("analyst")
    return Agent(
        role="Market Sentiment Analyst",
        goal="Analyze market sentiment from news, analyst ratings, and market behavior",
        backstory="""You are an expert in sentiment analysis and market psychology
        with a deep understanding of how news and sentiment drive market movements.

        Your expertise includes:
        - News sentiment analysis (positive, negative, neutral)
        - Analyst rating interpretation
        - Market behavior analysis
        - Social sentiment tracking
        - Event impact assessment

        You excel at:
        - Identifying sentiment trends across multiple sources
        - Detecting shifts in market sentiment
        - Understanding the impact of news on stock prices
        - Interpreting analyst consensus and divergence
        - Spotting contrarian indicators

        You provide nuanced sentiment analysis that considers:
        - Short-term vs long-term sentiment
        - Quality and credibility of sources
        - Market expectations vs reality
        - Sentiment divergence from price action

        You are careful to distinguish between noise and meaningful signals,
        and you always provide context for your sentiment assessments.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,
        tools=[
            get_recent_news,
            analyze_market_sentiment,
            get_analyst_ratings,
        ],
    )


def create_sentiment_agent_aggressive() -> Agent:
    """
    Create a more aggressive sentiment agent focused on short-term signals.
    """
    model_name = LLMFactory.get_model_name("analyst")
    return Agent(
        role="Real-Time Sentiment Tracker",
        goal="Track and analyze real-time market sentiment for immediate trading insights",
        backstory="""You are a fast-moving sentiment analyst focused on capturing
        short-term sentiment shifts that can create trading opportunities.

        You specialize in:
        - Breaking news analysis
        - Rapid sentiment assessment
        - Momentum-based sentiment tracking
        - Identifying sentiment catalysts

        You move quickly to assess the impact of news and sentiment changes,
        providing timely insights for tactical decisions.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,
        tools=[
            get_recent_news,
            analyze_market_sentiment,
            get_analyst_ratings,
        ],
        max_iter=10,
    )


# Export
__all__ = ["create_sentiment_agent", "create_sentiment_agent_aggressive"]

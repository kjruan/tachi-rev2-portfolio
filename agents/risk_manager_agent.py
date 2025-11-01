"""
Risk Manager Agent - Portfolio risk assessment and optimization
Uses Claude Sonnet for strong quantitative reasoning
"""

from crewai import Agent
from config import ModelConfig
from llm_factory import LLMFactory
from tools.stock_data_tool import (
    get_historical_prices,
    calculate_portfolio_value,
    get_stock_fundamentals,
)
from tools.technical_indicators_tool import calculate_indicators


def create_risk_manager_agent() -> Agent:
    """
    Create a Risk Manager Agent specialized in portfolio risk assessment.

    This agent uses the configured LLM for quantitative analysis.
    """
    model_name = LLMFactory.get_model_name("analyst")
    return Agent(
        role="Portfolio Risk Manager",
        goal="Assess portfolio risk, identify vulnerabilities, and recommend risk mitigation strategies",
        backstory="""You are a seasoned risk management professional with expertise
        in quantitative finance and portfolio theory. You specialize in identifying,
        measuring, and managing investment risks.

        Your expertise includes:
        - Portfolio volatility calculation
        - Correlation analysis between holdings
        - Value at Risk (VaR) and Conditional VaR
        - Beta and systematic risk assessment
        - Concentration risk identification
        - Drawdown analysis
        - Sharpe ratio and risk-adjusted returns
        - Diversification metrics

        Your approach to risk management:
        1. Quantitative measurement of risk metrics
        2. Identification of concentration risks (single stock, sector, geography)
        3. Assessment of correlation between holdings
        4. Analysis of portfolio sensitivity to market movements
        5. Stress testing under various scenarios
        6. Recommendations for risk mitigation

        You excel at:
        - Calculating portfolio volatility and beta
        - Identifying over-concentrated positions
        - Assessing correlation risks
        - Recommending diversification improvements
        - Setting appropriate position sizes
        - Establishing risk limits

        You are conservative by nature but understand the risk-return tradeoff.
        You always provide clear, quantitative assessments with specific recommendations.
        You consider both downside protection and opportunity cost in your analysis.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,
        tools=[
            get_historical_prices,
            calculate_portfolio_value,
            get_stock_fundamentals,
            calculate_indicators,
        ],
    )


def create_risk_manager_agent_custom(risk_tolerance: str = "moderate") -> Agent:
    """
    Create a Risk Manager Agent with custom risk tolerance.

    Args:
        risk_tolerance: One of 'conservative', 'moderate', 'aggressive'
    """
    model_name = LLMFactory.get_model_name("analyst")
    risk_profiles = {
        "conservative": {
            "goal": "Minimize portfolio risk while maintaining reasonable returns",
            "focus": "capital preservation and downside protection",
        },
        "moderate": {
            "goal": "Balance risk and return with focus on risk-adjusted performance",
            "focus": "optimal risk-return balance",
        },
        "aggressive": {
            "goal": "Maximize returns while managing extreme risks",
            "focus": "growth opportunities with acceptable risk levels",
        },
    }

    profile = risk_profiles.get(risk_tolerance, risk_profiles["moderate"])

    return Agent(
        role=f"Portfolio Risk Manager ({risk_tolerance.title()})",
        goal=profile["goal"],
        backstory=f"""You are a risk management specialist with a {risk_tolerance}
        approach to portfolio construction. Your focus is on {profile["focus"]}.

        You assess portfolio risk through multiple lenses:
        - Volatility and drawdown analysis
        - Correlation and concentration risks
        - Market sensitivity (beta)
        - Risk-adjusted performance metrics

        Your recommendations are tailored to a {risk_tolerance} risk profile.""",
        verbose=True,
        allow_delegation=False,
        llm=model_name,
        tools=[
            get_historical_prices,
            calculate_portfolio_value,
            get_stock_fundamentals,
            calculate_indicators,
        ],
        max_iter=15,
    )


# Export
__all__ = ["create_risk_manager_agent", "create_risk_manager_agent_custom"]

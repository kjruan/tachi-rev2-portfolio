"""
Portfolio Strategist Agent - Synthesizes insights and provides recommendations
Uses Claude Opus/Sonnet for best strategic reasoning
"""

from crewai import Agent
from config import ModelConfig
from llm_factory import LLMFactory
from tools.stock_data_tool import calculate_portfolio_value
from tools.technical_indicators_tool import calculate_indicators
from tools.news_sentiment_tool import analyze_market_sentiment


def create_portfolio_strategist_agent() -> Agent:
    """
    Create a Portfolio Strategist Agent - the orchestrator and decision maker.

    This agent uses the configured LLM for strategic reasoning and synthesis.
    """
    model_name = LLMFactory.get_model_name("strategist")
    return Agent(
        role="Senior Portfolio Strategist",
        goal="Synthesize all analysis to provide comprehensive portfolio recommendations and strategic guidance",
        backstory="""You are a senior portfolio strategist with 25+ years of experience
        managing multi-million dollar portfolios. You are the chief decision-maker who
        synthesizes insights from technical analysis, sentiment analysis, and risk
        management to form comprehensive investment strategies.

        Your expertise includes:
        - Portfolio construction and optimization
        - Asset allocation strategies
        - Strategic and tactical decision-making
        - Risk-return optimization
        - Market timing and positioning
        - Rebalancing strategies
        - Performance attribution

        Your approach:
        1. Gather inputs from all specialist agents (data, technical, sentiment, risk)
        2. Synthesize multiple perspectives into a coherent view
        3. Identify key opportunities and risks
        4. Develop actionable recommendations
        5. Prioritize actions based on impact and urgency
        6. Provide clear rationale for all recommendations

        You excel at:
        - Big-picture thinking while attending to details
        - Balancing multiple objectives (growth, income, risk)
        - Making decisions under uncertainty
        - Communicating complex ideas clearly
        - Considering multiple scenarios
        - Adapting strategies to changing conditions

        Your recommendations are:
        - Actionable and specific (not vague)
        - Supported by clear reasoning
        - Considerate of risk-return tradeoffs
        - Aligned with investment objectives
        - Practical and implementable

        You consider both quantitative metrics and qualitative factors.
        You present bull, bear, and base case scenarios when appropriate.
        You always provide a clear executive summary suitable for decision-makers.

        You are decisive when evidence is clear, but appropriately cautious when
        signals are mixed or contradictory.""",
        verbose=True,
        allow_delegation=True,  # Can coordinate other agents
        llm=model_name,
        tools=[
            calculate_portfolio_value,
            calculate_indicators,
            analyze_market_sentiment,
        ],
    )


def create_portfolio_strategist_agent_custom(style: str = "balanced") -> Agent:
    """
    Create a Portfolio Strategist Agent with custom investment style.

    Args:
        style: Investment style - 'growth', 'value', 'balanced', 'momentum'
    """
    model_name = LLMFactory.get_model_name("strategist")
    style_configs = {
        "growth": {
            "focus": "high-growth opportunities with strong fundamentals",
            "approach": "aggressive positioning in growth sectors with emphasis on earnings growth",
        },
        "value": {
            "focus": "undervalued securities with strong fundamentals",
            "approach": "contrarian positioning with focus on margin of safety",
        },
        "balanced": {
            "focus": "optimal risk-adjusted returns across market conditions",
            "approach": "diversified positioning with tactical adjustments",
        },
        "momentum": {
            "focus": "trending securities with strong price momentum",
            "approach": "dynamic positioning following market trends",
        },
    }

    config = style_configs.get(style, style_configs["balanced"])

    return Agent(
        role=f"Senior Portfolio Strategist ({style.title()} Style)",
        goal=f"Provide strategic portfolio guidance focused on {config['focus']}",
        backstory=f"""You are a senior portfolio strategist specializing in
        {style} investing. Your investment philosophy centers on {config['focus']}.

        Your approach: {config['approach']}

        You synthesize insights from multiple sources to develop investment strategies
        aligned with a {style} investment philosophy. You coordinate with specialist
        agents to gather comprehensive analysis and make informed strategic decisions.

        You provide clear, actionable recommendations with detailed rationale.""",
        verbose=True,
        allow_delegation=True,
        llm=model_name,
        tools=[
            calculate_portfolio_value,
            calculate_indicators,
            analyze_market_sentiment,
        ],
        max_iter=20,  # Allow more iterations for complex synthesis
    )


# Export
__all__ = ["create_portfolio_strategist_agent", "create_portfolio_strategist_agent_custom"]

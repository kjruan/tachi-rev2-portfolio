"""
Portfolio Analysis Crew - Orchestrates multi-agent portfolio analysis
"""

from crewai import Crew, Task, Process
from typing import Dict, List, Any
from agents import (
    create_data_fetcher_agent,
    create_market_analyst_agent,
    create_sentiment_agent,
    create_risk_manager_agent,
    create_portfolio_strategist_agent,
)


class PortfolioAnalysisCrew:
    """
    Orchestrates a team of AI agents to perform comprehensive portfolio analysis.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the portfolio analysis crew.

        Args:
            verbose: Whether to print detailed agent outputs
        """
        self.verbose = verbose

        # Initialize agents
        self.data_fetcher = create_data_fetcher_agent()
        self.market_analyst = create_market_analyst_agent()
        self.sentiment_analyst = create_sentiment_agent()
        self.risk_manager = create_risk_manager_agent()
        self.strategist = create_portfolio_strategist_agent()

    def analyze_portfolio(self, portfolio: Dict[str, float]) -> Dict[str, Any]:
        """
        Perform comprehensive portfolio analysis.

        Args:
            portfolio: Dictionary mapping ticker symbols to number of shares
                      Example: {'AAPL': 10, 'MSFT': 15, 'GOOGL': 5}

        Returns:
            Dictionary with comprehensive analysis results
        """
        tickers = list(portfolio.keys())
        ticker_list_str = ", ".join(tickers)

        # Task 1: Fetch portfolio data
        fetch_data_task = Task(
            description=f"""Fetch comprehensive data for the following portfolio:
            {portfolio}

            For each stock ({ticker_list_str}), retrieve:
            1. Current price and basic metrics
            2. Historical price data (90 days)
            3. Fundamental metrics (P/E, EPS, etc.)

            Also calculate the total portfolio value and allocation breakdown.

            Provide a well-structured summary of all data collected.""",
            agent=self.data_fetcher,
            expected_output="Structured data summary with prices, fundamentals, and portfolio value",
        )

        # Task 2: Technical analysis
        technical_analysis_task = Task(
            description=f"""Perform technical analysis on each stock in the portfolio: {ticker_list_str}

            For each stock, analyze:
            1. Technical indicators (RSI, MACD, Moving Averages, Bollinger Bands)
            2. Trend identification (uptrend, downtrend, consolidation)
            3. Momentum analysis
            4. Support and resistance levels

            Provide clear technical assessment for each position with:
            - Current trend status
            - Key technical levels
            - Technical signals (bullish/bearish/neutral)
            - Specific observations and concerns

            Summarize the overall technical picture of the portfolio.""",
            agent=self.market_analyst,
            expected_output="Technical analysis report for each stock with trend assessment and signals",
        )

        # Task 3: Sentiment analysis
        sentiment_analysis_task = Task(
            description=f"""Analyze market sentiment for each stock in the portfolio: {ticker_list_str}

            For each stock, assess:
            1. Recent news sentiment (last 10 articles)
            2. Analyst ratings and price targets
            3. Overall market sentiment
            4. Key sentiment drivers or concerns

            Provide sentiment assessment with:
            - Overall sentiment (bullish/bearish/neutral)
            - Key positive and negative factors
            - Potential sentiment catalysts
            - News highlights

            Summarize the sentiment landscape for the portfolio.""",
            agent=self.sentiment_analyst,
            expected_output="Sentiment analysis report with news assessment and analyst ratings",
        )

        # Task 4: Risk assessment
        risk_assessment_task = Task(
            description=f"""Assess the risk profile of this portfolio:
            {portfolio}

            Analyze:
            1. Individual stock volatility and risk metrics
            2. Portfolio concentration risk (check for over-concentration)
            3. Sector and industry exposure
            4. Historical volatility and drawdowns
            5. Beta and market sensitivity

            Provide risk assessment including:
            - Overall portfolio risk level (low/moderate/high)
            - Key risk factors and vulnerabilities
            - Concentration concerns
            - Risk metrics (volatility, beta where available)
            - Specific risk warnings

            Be thorough and identify any significant risks.""",
            agent=self.risk_manager,
            expected_output="Risk assessment report with concentration analysis and risk metrics",
        )

        # Task 5: Strategic synthesis
        strategy_synthesis_task = Task(
            description=f"""As the senior portfolio strategist, synthesize all analysis to provide
            comprehensive portfolio recommendations.

            Review the complete analysis from:
            - Data Fetcher: Portfolio composition and fundamentals
            - Technical Analyst: Technical signals and trends
            - Sentiment Analyst: News and market sentiment
            - Risk Manager: Risk assessment and vulnerabilities

            Provide a comprehensive strategic report including:

            1. **Executive Summary**
               - Overall portfolio health assessment
               - Key findings (3-5 bullets)
               - Immediate action items

            2. **Position-by-Position Analysis**
               - For each holding, provide: Hold/Buy More/Reduce/Sell recommendation
               - Clear rationale for each recommendation
               - Target allocation adjustments

            3. **Portfolio-Level Recommendations**
               - Rebalancing suggestions
               - Diversification improvements
               - Risk mitigation actions
               - Opportunities identified

            4. **Risk Considerations**
               - Key risks to monitor
               - Risk mitigation priorities
               - Market scenarios to watch

            5. **Action Plan**
               - Prioritized list of specific actions
               - Timeline for implementation
               - Success metrics

            Be specific, actionable, and clear. Provide concrete recommendations,
            not vague generalities.""",
            agent=self.strategist,
            expected_output="Comprehensive strategic report with specific recommendations and action plan",
        )

        # Create crew with sequential process
        crew = Crew(
            agents=[
                self.data_fetcher,
                self.market_analyst,
                self.sentiment_analyst,
                self.risk_manager,
                self.strategist,
            ],
            tasks=[
                fetch_data_task,
                technical_analysis_task,
                sentiment_analysis_task,
                risk_assessment_task,
                strategy_synthesis_task,
            ],
            process=Process.sequential,  # Tasks run in order
            verbose=self.verbose,
        )

        # Execute the crew
        result = crew.kickoff()

        return {
            "portfolio": portfolio,
            "analysis": str(result),
            "status": "completed",
        }

    def quick_analysis(self, ticker: str) -> Dict[str, Any]:
        """
        Perform quick analysis on a single stock.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with analysis results
        """
        # Quick data fetch
        data_task = Task(
            description=f"""Fetch current data for {ticker}:
            - Current price and basic metrics
            - Recent historical data (30 days)
            - Key fundamentals""",
            agent=self.data_fetcher,
            expected_output="Current stock data summary",
        )

        # Quick technical analysis
        technical_task = Task(
            description=f"""Perform quick technical analysis on {ticker}:
            - Key indicators (RSI, MACD, MAs)
            - Current trend
            - Technical signal (bullish/bearish/neutral)""",
            agent=self.market_analyst,
            expected_output="Technical analysis summary",
        )

        # Quick assessment
        assessment_task = Task(
            description=f"""Provide a quick investment assessment for {ticker}
            based on the data and technical analysis.

            Include:
            - Overall assessment (bullish/bearish/neutral)
            - Key positives and negatives
            - Recommendation (buy/hold/sell)""",
            agent=self.strategist,
            expected_output="Investment assessment with recommendation",
        )

        crew = Crew(
            agents=[self.data_fetcher, self.market_analyst, self.strategist],
            tasks=[data_task, technical_task, assessment_task],
            process=Process.sequential,
            verbose=self.verbose,
        )

        result = crew.kickoff()

        return {
            "ticker": ticker,
            "analysis": str(result),
            "status": "completed",
        }


# Export
__all__ = ["PortfolioAnalysisCrew"]

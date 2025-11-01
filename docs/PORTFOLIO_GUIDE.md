# Multi-Agent Portfolio Management with Claude

A comprehensive guide to building a personal portfolio management tool using Claude AI and multi-agent orchestration.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Agent Design](#agent-design)
6. [Implementation Guide](#implementation-guide)
7. [Usage Examples](#usage-examples)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)
10. [Resources](#resources)

---

## Overview

This project uses **multi-agent orchestration** to analyze investment portfolios. Multiple specialized AI agents work together, each powered by Claude AI models, to provide comprehensive portfolio analysis.

### Why Multi-Agent?

- **Specialization**: Each agent focuses on one domain (e.g., risk, sentiment, technical analysis)
- **Parallel Processing**: Agents can work simultaneously
- **Modularity**: Easy to add/remove/modify agents
- **Better Results**: Specialized agents outperform single monolithic systems

### Key Benefits

- ✅ Comprehensive portfolio analysis
- ✅ Real-time market sentiment tracking
- ✅ Risk assessment and recommendations
- ✅ Automated rebalancing suggestions
- ✅ No per-usage costs (with Claude Max plan)

---

## Architecture

### Agent Team Structure

```
┌─────────────────────────────────────────┐
│     Portfolio Strategist (Orchestrator)  │
│         Claude Opus 4 / Sonnet 4.5      │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼─────────┐
│ Market Analyst │  │ News Sentiment │
│ Claude Sonnet  │  │ Claude Sonnet  │
└───────┬────────┘  └──────┬─────────┘
        │                   │
        └─────────┬─────────┘
                  │
        ┌─────────▼──────────┐
        │   Risk Manager     │
        │   Claude Sonnet    │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │   Data Fetcher     │
        │   Claude Haiku     │
        └────────────────────┘
```

### Data Flow

1. **Input**: User provides portfolio (ticker symbols, quantities)
2. **Data Fetching**: Data agent retrieves current prices, historical data
3. **Parallel Analysis**: 
   - Market Analyst: Technical indicators, trends
   - News Sentiment: Current market sentiment
   - Risk Manager: Volatility, correlation, risk metrics
4. **Synthesis**: Portfolio Strategist combines insights
5. **Output**: Comprehensive report with recommendations

---

## Prerequisites

### Required Accounts

- **Claude Max Plan** (includes API access)
  - Get your API key from: https://console.anthropic.com/

### Required Software

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Required Python Packages

```bash
crewai>=0.28.0
crewai-tools>=0.1.0
langchain-anthropic>=0.1.0
python-dotenv>=1.0.0
yfinance>=0.2.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
```

---

## Setup Instructions

### 1. Create Project Directory

```bash
mkdir portfolio-agent
cd portfolio-agent
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install crewai crewai-tools langchain-anthropic python-dotenv yfinance pandas numpy requests
```

### 4. Configure API Keys

Create a `.env` file in your project root:

```bash
ANTHROPIC_API_KEY=your_claude_api_key_here
```

**To get your Claude API key:**
1. Go to https://console.anthropic.com/
2. Navigate to API Keys
3. Create a new key or copy existing one
4. Paste into `.env` file

### 5. Project Structure

```
portfolio-agent/
├── .env                    # API keys (DO NOT COMMIT)
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── claude.md             # This documentation
├── agents/
│   ├── __init__.py
│   ├── market_analyst.py
│   ├── news_sentiment.py
│   ├── risk_manager.py
│   └── strategist.py
├── tools/
│   ├── __init__.py
│   ├── stock_data.py
│   └── news_fetcher.py
├── main.py               # Main orchestration script
└── config.py             # Configuration settings
```

---

## Agent Design

### 1. Data Fetcher Agent

**Role**: Retrieve stock data and financial metrics

**Model**: Claude Haiku 3.5 (fast, efficient for simple tasks)

**Responsibilities**:
- Fetch current stock prices
- Get historical price data
- Retrieve company fundamentals
- Calculate basic metrics (P/E, market cap, etc.)

**Tools**:
- Yahoo Finance API (`yfinance`)
- Financial data APIs

### 2. Market Analyst Agent

**Role**: Technical analysis and trend identification

**Model**: Claude Sonnet 4.5 (strong analytical capabilities)

**Responsibilities**:
- Calculate technical indicators (RSI, MACD, Moving Averages)
- Identify chart patterns
- Analyze price trends
- Detect support/resistance levels

**Key Metrics**:
- 50-day and 200-day moving averages
- Relative Strength Index (RSI)
- Volume trends
- Price momentum

### 3. News Sentiment Agent

**Role**: Market sentiment analysis from news sources

**Model**: Claude Sonnet 4.5 (excellent at NLP and sentiment analysis)

**Responsibilities**:
- Aggregate recent news articles
- Analyze sentiment (positive/negative/neutral)
- Identify key events affecting stocks
- Track social media sentiment

**Data Sources**:
- Financial news APIs
- RSS feeds
- Social media (Twitter/X financial discussions)

### 4. Risk Manager Agent

**Role**: Portfolio risk assessment and optimization

**Model**: Claude Sonnet 4.5 (strong quantitative reasoning)

**Responsibilities**:
- Calculate portfolio volatility
- Assess correlation between holdings
- Compute Value at Risk (VaR)
- Identify concentration risks
- Suggest diversification improvements

**Key Metrics**:
- Standard deviation (volatility)
- Beta (market correlation)
- Sharpe ratio
- Maximum drawdown
- Portfolio correlation matrix

### 5. Portfolio Strategist Agent (Orchestrator)

**Role**: Synthesize insights and provide recommendations

**Model**: Claude Opus 4 or Sonnet 4.5 (best reasoning for strategy)

**Responsibilities**:
- Coordinate other agents
- Synthesize all analysis
- Generate actionable recommendations
- Create comprehensive reports
- Suggest portfolio rebalancing

**Output Format**:
- Executive summary
- Detailed analysis by agent
- Specific action items
- Risk warnings
- Timeline for next review

---

## Implementation Guide

### Basic CrewAI Setup

```python
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Claude models
claude_opus = ChatAnthropic(
    model="claude-opus-4-20250514",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.7
)

claude_sonnet = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.5
)

claude_haiku = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.3
)
```

### Creating an Agent

```python
market_analyst = Agent(
    role='Market Data Analyst',
    goal='Analyze stock performance, trends, and technical indicators',
    backstory="""You are an expert technical analyst with 20 years of 
    experience in equity markets. You specialize in identifying trends, 
    support/resistance levels, and technical patterns.""",
    llm=claude_sonnet,
    verbose=True,
    allow_delegation=False,
    tools=[stock_data_tool, technical_indicators_tool]
)
```

### Creating a Task

```python
analyze_market_task = Task(
    description="""Analyze the following stocks: {stocks}
    
    For each stock, provide:
    1. Current price and 52-week range
    2. Key technical indicators (RSI, MACD, Moving Averages)
    3. Trend analysis (bullish/bearish/neutral)
    4. Support and resistance levels
    5. Volume analysis
    
    Format your response clearly with headers for each stock.""",
    agent=market_analyst,
    expected_output="Detailed technical analysis for each stock"
)
```

### Creating the Crew

```python
portfolio_crew = Crew(
    agents=[
        data_fetcher,
        market_analyst,
        news_sentiment_agent,
        risk_manager,
        portfolio_strategist
    ],
    tasks=[
        fetch_data_task,
        analyze_market_task,
        sentiment_task,
        risk_assessment_task,
        strategy_task
    ],
    verbose=True,
    process=Process.sequential  # or Process.hierarchical
)
```

### Running the Analysis

```python
# Define your portfolio
portfolio = {
    'stocks': ['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
    'shares': [10, 15, 5, 8]
}

# Execute the crew
result = portfolio_crew.kickoff(inputs=portfolio)

# Display results
print(result)
```

---

## Usage Examples

### Example 1: Simple Portfolio Analysis

```python
# Analyze a basic portfolio
portfolio = {
    'stocks': ['AAPL', 'MSFT', 'NVDA'],
    'shares': [50, 30, 20]
}

result = portfolio_crew.kickoff(inputs=portfolio)
```

### Example 2: Risk-Focused Analysis

```python
# Focus on risk assessment
risk_focused_task = Task(
    description="""Perform deep risk analysis on portfolio: {stocks}
    
    Focus on:
    - Portfolio volatility
    - Correlation risks
    - Sector concentration
    - Tail risk (VaR, CVaR)
    - Stress testing scenarios
    """,
    agent=risk_manager,
    expected_output="Comprehensive risk report"
)
```

### Example 3: Rebalancing Recommendations

```python
# Get rebalancing suggestions
rebalance_task = Task(
    description="""Given current portfolio {stocks} with allocations {shares},
    recommend optimal rebalancing to:
    1. Reduce concentration risk
    2. Improve risk-adjusted returns
    3. Align with target allocation of 60% large-cap, 40% tech
    
    Provide specific buy/sell recommendations.""",
    agent=portfolio_strategist,
    expected_output="Rebalancing action plan"
)
```

---

## Advanced Features

### 1. Custom Tools

Create specialized tools for your agents:

```python
from crewai_tools import tool

@tool("Get Stock Fundamentals")
def get_fundamentals(ticker: str) -> dict:
    """Fetch fundamental data for a stock ticker"""
    import yfinance as yf
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        'pe_ratio': info.get('trailingPE'),
        'market_cap': info.get('marketCap'),
        'revenue': info.get('totalRevenue'),
        'profit_margin': info.get('profitMargins')
    }
```

### 2. Memory and Context

Enable agents to remember previous analyses:

```python
from crewai import Agent

agent_with_memory = Agent(
    role='Portfolio Strategist',
    goal='Track portfolio performance over time',
    memory=True,  # Enable memory
    verbose=True,
    llm=claude_opus
)
```

### 3. Parallel Processing

Run independent agents in parallel:

```python
from crewai import Crew, Process

parallel_crew = Crew(
    agents=[market_analyst, news_sentiment_agent],
    tasks=[market_task, sentiment_task],
    process=Process.parallel  # Run simultaneously
)
```

### 4. Hierarchical Orchestration

Create a manager-worker structure:

```python
manager_agent = Agent(
    role='Portfolio Manager',
    goal='Oversee all portfolio analysis',
    llm=claude_opus,
    allow_delegation=True  # Can delegate to other agents
)

hierarchical_crew = Crew(
    agents=[manager_agent, market_analyst, risk_manager],
    tasks=[analysis_task],
    process=Process.hierarchical,
    manager_llm=claude_opus
)
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Errors

**Problem**: `AuthenticationError: Invalid API key`

**Solution**:
- Verify your API key in `.env` file
- Ensure `.env` is in the project root
- Check that `load_dotenv()` is called before initializing Claude

#### 2. Rate Limiting

**Problem**: `RateLimitError: Too many requests`

**Solution**:
- Add delays between requests
- Implement exponential backoff
- With Claude Max, this should be rare

```python
import time
time.sleep(1)  # Add 1-second delay between calls
```

#### 3. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'crewai'`

**Solution**:
```bash
pip install --upgrade crewai crewai-tools
```

#### 4. Stock Data Issues

**Problem**: `KeyError` when fetching stock data

**Solution**:
- Verify ticker symbols are correct
- Check if market is open
- Add error handling:

```python
try:
    data = yf.download(ticker)
except Exception as e:
    print(f"Error fetching {ticker}: {e}")
```

---

## Resources

### Documentation

- **CrewAI Docs**: https://docs.crewai.com/
- **Claude API Docs**: https://docs.anthropic.com/
- **LangChain Anthropic**: https://python.langchain.com/docs/integrations/chat/anthropic

### Sample Code Repositories

- CrewAI Examples: https://github.com/joaomdmoura/crewAI-examples
- Financial Analysis with AI: https://github.com/topics/financial-analysis

### Learning Resources

- CrewAI YouTube Tutorials
- Multi-Agent Systems Research Papers
- Anthropic Claude Cookbook

### Financial Data APIs

- **Yahoo Finance**: Free, good for historical data
- **Alpha Vantage**: Free tier available
- **IEX Cloud**: Real-time market data
- **Finnhub**: News and sentiment data

### Community

- CrewAI Discord: Join for support
- Reddit: r/LangChain, r/ClaudeAI
- Stack Overflow: Tag `crewai` or `claude-ai`

---

## Next Steps

### Immediate Actions

1. ✅ Set up development environment
2. ✅ Configure Claude API key
3. ✅ Install dependencies
4. ✅ Test basic agent creation
5. ✅ Build first simple portfolio analyzer

### Short-term Goals (Week 1-2)

- [ ] Implement all 5 core agents
- [ ] Create custom stock data tools
- [ ] Test with sample portfolio
- [ ] Refine agent prompts for better output
- [ ] Add error handling and logging

### Medium-term Goals (Week 3-4)

- [ ] Add news sentiment analysis
- [ ] Implement risk calculations
- [ ] Create formatted report output
- [ ] Add visualization (charts, graphs)
- [ ] Build simple CLI interface

### Long-term Ideas

- [ ] Web interface (Streamlit/Gradio)
- [ ] Automated daily reports
- [ ] Portfolio tracking over time
- [ ] Backtesting capabilities
- [ ] Integration with brokerage APIs
- [ ] Mobile notifications for alerts

---

## Contributing

This is a personal project, but feel free to:

- Fork and modify for your needs
- Share improvements and ideas
- Report bugs or issues
- Suggest new features

---

## License

This project is for personal use. Ensure compliance with:
- Claude AI Terms of Service
- Financial data provider terms
- Securities regulations (if sharing investment advice)

---

**Last Updated**: October 2025

**Version**: 1.0.0

**Author**: Your Name

---

## Quick Reference

### Essential Commands

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run analysis
python main.py

# Deactivate environment
deactivate
```

### Key Configuration

```python
# Model selection guide
claude_opus = "claude-opus-4-20250514"      # Best reasoning
claude_sonnet = "claude-sonnet-4-20250514"  # Balanced
claude_haiku = "claude-3-5-haiku-20241022"  # Fast & cheap
```

---

*Happy investing with AI! 📈🤖*

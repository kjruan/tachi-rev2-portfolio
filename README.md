# Rev2 - AI-Powered Portfolio Management System

A sophisticated multi-agent portfolio analysis system powered by Claude AI and CrewAI. Rev2 uses specialized AI agents to provide comprehensive portfolio analysis, technical insights, sentiment assessment, and risk management recommendations.

## Features

- **Multi-Agent Architecture**: Five specialized AI agents working together
- **Comprehensive Analysis**: Technical, sentiment, and risk analysis
- **Claude AI Powered**: Uses Claude Opus, Sonnet, and Haiku models
- **Standalone Application**: Can run independently or integrate with tachi-cli
- **API-First Design**: RESTful API for easy integration
- **Interactive CLI**: Beautiful terminal interface for direct use

## Architecture

### Specialized Agents

1. **Data Fetcher Agent** (Claude Haiku)
   - Retrieves stock prices and market data
   - Gathers fundamental metrics
   - Calculates portfolio values

2. **Market Analyst Agent** (Claude Sonnet)
   - Technical indicator analysis (RSI, MACD, MAs, Bollinger Bands)
   - Trend identification
   - Support/resistance detection
   - Momentum analysis

3. **Sentiment Analyst Agent** (Claude Sonnet)
   - News sentiment analysis
   - Analyst rating interpretation
   - Market sentiment assessment

4. **Risk Manager Agent** (Claude Sonnet)
   - Portfolio risk assessment
   - Concentration risk analysis
   - Volatility and correlation analysis
   - Risk-adjusted metrics

5. **Portfolio Strategist Agent** (Claude Opus/Sonnet)
   - Synthesizes all insights
   - Generates actionable recommendations
   - Creates comprehensive reports
   - Provides strategic guidance

## Installation

### Prerequisites

- Python 3.9 or higher
- Claude API key (get from [console.anthropic.com](https://console.anthropic.com/))
- uv package manager (recommended) or pip

### Setup Steps

1. **Navigate to rev2 directory**:
   ```bash
   cd rev2
   ```

2. **Create and activate virtual environment using uv**:
   ```bash
   # Virtual environment is already created
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Configure API keys**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

4. **Verify installation**:
   ```bash
   python config.py
   ```

## Usage

### CLI Interface

Run the interactive CLI:

```bash
python main.py
```

#### CLI Features

- **Analyze Portfolio**: Input multiple stocks with share counts
- **Quick Stock Analysis**: Analyze a single stock
- **Example Portfolios**: Pre-configured examples for testing
- **Configuration Check**: Verify system setup

#### Example: Analyze a Portfolio

```bash
$ python main.py
# Select option 1: Analyze Portfolio
# Enter stocks:
AAPL:10
MSFT:15
GOOGL:5
done
```

### API Server

Start the FastAPI server for programmatic access:

```bash
python api/server.py
```

The server will start on `http://0.0.0.0:8001`

API Documentation available at: `http://localhost:8001/docs`

#### API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /api/v1/portfolio/analyze` - Analyze portfolio
- `POST /api/v1/stock/analyze` - Analyze single stock
- `GET /api/v1/tasks/{task_id}` - Get task status
- `GET /api/v1/tasks` - List recent tasks

#### Example API Usage

```python
import requests

# Analyze portfolio
response = requests.post(
    "http://localhost:8001/api/v1/portfolio/analyze",
    json={
        "portfolio": {
            "AAPL": 10,
            "MSFT": 15,
            "GOOGL": 5
        }
    }
)

task_id = response.json()["task_id"]

# Check status
status = requests.get(f"http://localhost:8001/api/v1/tasks/{task_id}")
print(status.json())
```

## Configuration

### Environment Variables (.env)

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional - Model preferences
DEFAULT_STRATEGIST_MODEL=claude-sonnet-4-20250514
DEFAULT_ANALYST_MODEL=claude-sonnet-4-20250514
DEFAULT_FETCHER_MODEL=claude-3-5-haiku-20241022

# Optional - API server settings
API_HOST=0.0.0.0
API_PORT=8001

# Optional - Logging
LOG_LEVEL=INFO
```

### Model Configuration

The system uses three Claude models optimized for different tasks:

- **Claude Opus 4**: Strategic reasoning (Portfolio Strategist)
- **Claude Sonnet 4.5**: Analysis (Market Analyst, Sentiment, Risk)
- **Claude Haiku 3.5**: Fast data retrieval (Data Fetcher)

## Integration with Tachi-CLI

Rev2 is designed to integrate with the main tachi-cli application through its API:

```python
# In tachi-cli
import requests

# Call rev2 API
rev2_api = "http://localhost:8001"
response = requests.post(
    f"{rev2_api}/api/v1/portfolio/analyze",
    json={"portfolio": portfolio_data}
)
```

## Project Structure

```
rev2/
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Environment template
├── .gitignore             # Git ignore rules
├── .venv/                 # Virtual environment (uv)
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md              # This file
├── config.py              # Configuration & model setup
├── main.py                # CLI interface
│
├── agents/                # AI agent definitions
│   ├── __init__.py
│   ├── data_fetcher_agent.py
│   ├── market_analyst_agent.py
│   ├── sentiment_agent.py
│   ├── risk_manager_agent.py
│   └── portfolio_strategist_agent.py
│
├── tools/                 # Custom tools for agents
│   ├── __init__.py
│   ├── stock_data_tool.py
│   ├── technical_indicators_tool.py
│   └── news_sentiment_tool.py
│
├── crews/                 # Crew orchestration
│   ├── __init__.py
│   └── portfolio_crew.py
│
├── api/                   # FastAPI server
│   ├── __init__.py
│   └── server.py
│
└── tests/                 # Unit tests
    └── __init__.py
```

## Development

### Running Tests

```bash
# Install dev dependencies
uv pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Adding Custom Tools

Create a new tool in `tools/`:

```python
from crewai_tools import tool

@tool("My Custom Tool")
def my_custom_tool(param: str) -> dict:
    """Tool description"""
    # Implementation
    return {"result": "data"}
```

### Creating Custom Agents

Extend or modify agents in `agents/`:

```python
from crewai import Agent
from config import ModelConfig

def create_custom_agent() -> Agent:
    return Agent(
        role="Custom Role",
        goal="Custom goal",
        backstory="Agent backstory...",
        llm=ModelConfig.get_analyst_model(),
        tools=[tool1, tool2],
    )
```

## Troubleshooting

### Common Issues

**1. API Key Not Found**
```bash
# Error: ANTHROPIC_API_KEY not found
# Solution: Check .env file exists and has valid API key
cp .env.example .env
# Edit .env and add your key
```

**2. Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Activate virtual environment
source .venv/bin/activate
```

**3. Connection Errors**
```bash
# Error: Cannot connect to API
# Solution: Check Claude API status and key validity
python config.py  # Verify configuration
```

## Performance

- **Full Portfolio Analysis**: 2-5 minutes (depends on portfolio size)
- **Quick Stock Analysis**: 30-90 seconds
- **API Response**: Immediate (async processing)

## Limitations

- Free tier Claude API has rate limits
- News sentiment uses yfinance (limited data)
- Historical data limited to yfinance availability
- In-memory task storage (not persistent)

## Future Enhancements

- [ ] Persistent task storage (database)
- [ ] Real-time price updates
- [ ] Advanced news APIs integration
- [ ] Portfolio optimization algorithms
- [ ] Backtesting capabilities
- [ ] Email/webhook notifications
- [ ] Performance tracking over time
- [ ] Machine learning price predictions

## License

Part of the tachi-cli project. See main project LICENSE.

## Support

For issues or questions:
1. Check this README
2. Review [context/REV2_PORTFOLIO_GUIDE.md](../context/REV2_PORTFOLIO_GUIDE.md)
3. Check Claude API documentation
4. Review tachi-cli main documentation

## Credits

- **AI Framework**: CrewAI
- **Language Models**: Claude AI by Anthropic
- **Market Data**: yfinance   
- **Web Framework**: FastAPI

---

**Note**: Rev2 is designed for research and educational purposes. Always conduct thorough due diligence before making investment decisions.

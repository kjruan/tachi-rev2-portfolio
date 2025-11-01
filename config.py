"""
Configuration for rev2 Portfolio Management System
Multi-Provider Support: Ollama, OpenRouter, Groq, Claude
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LLM factory for multi-provider support
from llm_factory import LLMFactory, get_strategist_model, get_analyst_model, get_fetcher_model

# Model Configuration
class ModelConfig:
    """Multi-provider model configurations for different agents"""

    # Temperature settings
    TEMP_CREATIVE = 0.7  # For strategic thinking
    TEMP_BALANCED = 0.5  # For analysis
    TEMP_PRECISE = 0.3   # For data fetching

    @classmethod
    def get_strategist_model(cls):
        """Portfolio Strategist - Uses best available model for reasoning"""
        return get_strategist_model()

    @classmethod
    def get_analyst_model(cls):
        """Market Analyst - Uses balanced model for analysis"""
        return get_analyst_model()

    @classmethod
    def get_sentiment_model(cls):
        """News Sentiment Agent - Uses model optimized for NLP"""
        return get_analyst_model()

    @classmethod
    def get_risk_model(cls):
        """Risk Manager - Uses model for quantitative analysis"""
        return get_analyst_model()

    @classmethod
    def get_fetcher_model(cls):
        """Data Fetcher - Uses fast model for simple tasks"""
        return get_fetcher_model()


# API Server Configuration
class APIConfig:
    """API server settings for future tachi integration"""

    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "8001"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # CORS settings
    CORS_ORIGINS = [
        "http://localhost:3000",  # tachi-web frontend
        "http://localhost:5000",  # tachi main app
    ]


# Logging Configuration
class LogConfig:
    """Logging settings"""

    LEVEL = os.getenv("LOG_LEVEL", "INFO")
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# Portfolio Analysis Configuration
class AnalysisConfig:
    """Default settings for portfolio analysis"""

    # Historical data period for analysis
    DEFAULT_LOOKBACK_DAYS = 90

    # Risk-free rate for Sharpe ratio calculation
    RISK_FREE_RATE = 0.04  # 4% annual

    # Number of simulation runs for Monte Carlo
    MONTE_CARLO_SIMULATIONS = 1000

    # Confidence levels for risk metrics
    VAR_CONFIDENCE_LEVEL = 0.95  # 95% VaR

    # Rebalancing thresholds
    REBALANCE_THRESHOLD = 0.05  # 5% drift from target


# Export commonly used objects
models = ModelConfig()
api_config = APIConfig()
log_config = LogConfig()
analysis_config = AnalysisConfig()


def verify_setup() -> bool:
    """Verify that the configuration is valid"""
    try:
        # Check if provider is configured
        provider = LLMFactory.get_provider()

        if not LLMFactory.verify_provider():
            print(f"ERROR: {provider} provider not configured or unavailable")
            print(f"\nPlease configure one of the following providers in .env:")
            print(f"  - Ollama: Install from https://ollama.ai (local/free)")
            print(f"  - OpenRouter: Set OPENROUTER_API_KEY (free tier available)")
            print(f"  - Groq: Set GROQ_API_KEY (free tier available)")
            print(f"  - Claude: Set ANTHROPIC_API_KEY (paid)")
            return False

        # Try to initialize a model
        test_model = models.get_fetcher_model()

        # List available providers
        available = LLMFactory.list_available_providers()
        available_list = [p for p, avail in available.items() if avail]

        print(f"Configuration verified successfully")
        print(f"\nActive Provider: {provider}")
        print(f"Available Providers: {', '.join(available_list)}")
        print(f"\nModel Configuration:")
        print(f"  - Strategist: {LLMFactory.get_model_name('strategist')}")
        print(f"  - Analyst: {LLMFactory.get_model_name('analyst')}")
        print(f"  - Fetcher: {LLMFactory.get_model_name('fetcher')}")
        return True

    except Exception as e:
        print(f"Configuration error: {e}")
        return False


if __name__ == "__main__":
    # Test configuration
    print("Testing rev2 configuration...")
    if verify_setup():
        print("Configuration is valid!")
    else:
        print("Configuration failed!")

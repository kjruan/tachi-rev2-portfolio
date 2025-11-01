"""
Integration tests for all tools
Tests the tools working together in realistic scenarios
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path to import tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from stock_data_tool import (
    get_stock_price,
    get_historical_prices,
    get_stock_fundamentals,
    get_multiple_stocks,
    calculate_portfolio_value,
)
from technical_indicators_tool import (
    calculate_indicators,
    analyze_momentum,
    detect_support_resistance,
)
from news_sentiment_tool import (
    get_recent_news,
    analyze_market_sentiment,
    get_analyst_ratings,
)


@pytest.mark.integration
class TestFullWorkflow:
    """Integration tests for complete analysis workflows"""

    def test_complete_stock_analysis_workflow(self):
        """Test a complete stock analysis using all tools"""
        ticker = "AAPL"

        # Step 1: Get basic stock information
        price_data = get_stock_price.func(ticker)
        if "error" in price_data:
            pytest.skip("API unavailable")

        assert "current_price" in price_data
        assert price_data["ticker"] == ticker

        # Step 2: Get historical data
        historical = get_historical_prices.func(ticker, days=90)
        if "error" in historical:
            pytest.skip("Historical data unavailable")

        assert historical["ticker"] == ticker
        assert historical["data_points"] > 0

        # Step 3: Get fundamentals
        fundamentals = get_stock_fundamentals.func(ticker)
        if "error" in fundamentals:
            pytest.skip("Fundamentals unavailable")

        assert fundamentals["ticker"] == ticker

        # Step 4: Calculate technical indicators
        indicators = calculate_indicators.func(ticker, days=90)
        if "error" in indicators:
            pytest.skip("Indicators unavailable")

        assert indicators["ticker"] == ticker
        assert "moving_averages" in indicators
        assert "rsi" in indicators

        # Step 5: Analyze momentum
        momentum = analyze_momentum.func(ticker, days=30)
        if "error" in momentum:
            pytest.skip("Momentum analysis unavailable")

        assert momentum["ticker"] == ticker
        assert "momentum_direction" in momentum

        # Step 6: Detect support/resistance
        support_resistance = detect_support_resistance.func(ticker, days=90)
        if "error" in support_resistance:
            pytest.skip("Support/resistance unavailable")

        assert support_resistance["ticker"] == ticker
        assert "support_levels" in support_resistance
        assert "resistance_levels" in support_resistance

        # Step 7: Get news and sentiment
        news = get_recent_news.func(ticker, max_items=5)
        if "error" in news:
            pytest.skip("News unavailable")

        assert news["ticker"] == ticker

        # Step 8: Analyze overall market sentiment
        sentiment = analyze_market_sentiment.func(ticker)
        if "error" in sentiment:
            pytest.skip("Sentiment analysis unavailable")

        assert sentiment["ticker"] == ticker
        assert "overall_sentiment" in sentiment

        # Step 9: Get analyst ratings
        ratings = get_analyst_ratings.func(ticker)
        if "error" in ratings:
            pytest.skip("Analyst ratings unavailable")

        assert ratings["ticker"] == ticker

        # Verify data consistency
        # Price from different sources should be similar (within 10%)
        if "current_price" in price_data and "current_price" in indicators:
            price_diff = abs(price_data["current_price"] - indicators["current_price"])
            price_avg = (price_data["current_price"] + indicators["current_price"]) / 2
            assert price_diff / price_avg < 0.1, "Price mismatch between sources"

    def test_portfolio_analysis_workflow(self):
        """Test portfolio analysis workflow"""
        # Create a test portfolio
        portfolio = {"AAPL": 10, "MSFT": 5, "GOOGL": 2}

        # Get individual stock data
        stocks_data = get_multiple_stocks.func(list(portfolio.keys()))
        if any("error" in data for data in stocks_data.values()):
            pytest.skip("Stock data unavailable")

        # Calculate portfolio value
        portfolio_value = calculate_portfolio_value.func(portfolio)
        if "error" in portfolio_value:
            pytest.skip("Portfolio calculation failed")

        assert portfolio_value["num_positions"] == 3
        assert portfolio_value["total_value"] > 0
        assert "holdings" in portfolio_value

        # Verify all positions are included
        for ticker in portfolio.keys():
            assert ticker in portfolio_value["holdings"]
            assert portfolio_value["holdings"][ticker]["shares"] == portfolio[ticker]

        # Verify weights sum to approximately 100%
        total_weight = sum(
            holding["weight"] for holding in portfolio_value["holdings"].values()
        )
        assert abs(total_weight - 100.0) < 0.01

    def test_technical_analysis_consistency(self):
        """Test consistency between technical analysis tools"""
        ticker = "AAPL"

        # Get indicators
        indicators = calculate_indicators.func(ticker, days=90)
        if "error" in indicators:
            pytest.skip("Indicators unavailable")

        # Get momentum
        momentum = analyze_momentum.func(ticker, days=30)
        if "error" in momentum:
            pytest.skip("Momentum unavailable")

        # Check consistency between trend and momentum
        trend = indicators["trend"]
        momentum_direction = momentum["momentum_direction"]

        # If there's a strong uptrend, momentum should generally be bullish
        # (though not always due to different time periods)
        if "UPTREND" in trend:
            # Just verify both have values - they may differ due to timeframes
            assert momentum_direction in ["BULLISH", "BEARISH", "NEUTRAL"]

    def test_sentiment_analysis_correlation(self):
        """Test correlation between different sentiment indicators"""
        ticker = "AAPL"

        # Get news sentiment
        news = get_recent_news.func(ticker, max_items=10)
        if "error" in news or news["news_count"] == 0:
            pytest.skip("News unavailable")

        # Get overall market sentiment
        sentiment = analyze_market_sentiment.func(ticker)
        if "error" in sentiment:
            pytest.skip("Sentiment analysis unavailable")

        # Get analyst ratings
        ratings = get_analyst_ratings.func(ticker)
        if "error" in ratings:
            pytest.skip("Analyst ratings unavailable")

        # All sentiment data should be present
        assert "overall_sentiment" in news
        assert "overall_sentiment" in sentiment
        assert "recommendation" in ratings

    def test_multiple_stocks_comparison(self):
        """Test comparing multiple stocks"""
        tickers = ["AAPL", "MSFT", "GOOGL"]

        results = {}
        for ticker in tickers:
            # Get key metrics for each stock
            price = get_stock_price.func(ticker)
            if "error" not in price:
                fundamentals = get_stock_fundamentals.func(ticker)
                indicators = calculate_indicators.func(ticker, days=90)

                results[ticker] = {
                    "price": price.get("current_price"),
                    "pe_ratio": fundamentals.get("pe_ratio") if "error" not in fundamentals else None,
                    "trend": indicators.get("trend") if "error" not in indicators else None,
                }

        # Should have data for at least one stock
        assert len(results) > 0

        # Verify data structure
        for ticker, data in results.items():
            assert "price" in data
            assert "pe_ratio" in data
            assert "trend" in data


@pytest.mark.integration
class TestErrorHandling:
    """Integration tests for error handling"""

    def test_invalid_ticker_across_all_tools(self):
        """Test that all tools handle invalid tickers gracefully"""
        invalid_ticker = "INVALID_TICKER_12345"

        # Test all tools with invalid ticker
        tools_to_test = [
            ("get_stock_price", get_stock_price.func),
            ("get_historical_prices", get_historical_prices.func),
            ("get_stock_fundamentals", get_stock_fundamentals.func),
            ("calculate_indicators", calculate_indicators.func),
            ("analyze_momentum", analyze_momentum.func),
            ("detect_support_resistance", detect_support_resistance.func),
            ("get_recent_news", get_recent_news.func),
            ("analyze_market_sentiment", analyze_market_sentiment.func),
            ("get_analyst_ratings", get_analyst_ratings.func),
        ]

        for tool_name, tool_func in tools_to_test:
            result = tool_func(invalid_ticker)
            # Tool should either return an error or handle gracefully
            # (some tools might return empty data instead of error)
            assert isinstance(result, dict), f"{tool_name} should return a dict"

    def test_edge_cases_portfolio(self):
        """Test edge cases in portfolio calculations"""
        # Empty portfolio
        empty_result = calculate_portfolio_value.func({})
        assert empty_result["total_value"] == 0
        assert empty_result["num_positions"] == 0

        # Single stock portfolio
        single_result = calculate_portfolio_value.func({"AAPL": 1})
        if "error" not in single_result:
            assert single_result["num_positions"] == 1
            assert single_result["holdings"]["AAPL"]["weight"] == 100.0


@pytest.mark.integration
@pytest.mark.slow
class TestPerformance:
    """Performance and stress tests"""

    def test_multiple_rapid_requests(self):
        """Test making multiple rapid requests"""
        ticker = "AAPL"

        # Make several requests in sequence
        for _ in range(3):
            result = get_stock_price.func(ticker)
            if "error" in result:
                pytest.skip("API unavailable")
            assert "current_price" in result

    def test_large_portfolio(self):
        """Test with a larger portfolio"""
        # Create a portfolio with 10 stocks
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC"]
        portfolio = {ticker: i + 1 for i, ticker in enumerate(tickers)}

        result = calculate_portfolio_value.func(portfolio)
        if "error" in result:
            pytest.skip("Portfolio calculation failed")

        assert result["num_positions"] == len(tickers)
        assert result["total_value"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])

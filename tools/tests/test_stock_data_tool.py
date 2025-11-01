"""
Unit tests for stock_data_tool.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import pandas as pd
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


class TestGetStockPrice:
    """Tests for get_stock_price tool"""

    @patch("stock_data_tool.yf.Ticker")
    def test_get_stock_price_success(self, mock_ticker):
        """Test successful stock price retrieval"""
        # Mock the ticker info
        mock_info = {
            "currentPrice": 150.00,
            "previousClose": 148.00,
            "regularMarketChange": 2.00,
            "regularMarketChangePercent": 1.35,
            "volume": 50000000,
            "marketCap": 2500000000000,
            "fiftyTwoWeekHigh": 180.00,
            "fiftyTwoWeekLow": 120.00,
        }
        mock_ticker.return_value.info = mock_info

        result = get_stock_price.func("AAPL")

        assert result["ticker"] == "AAPL"
        assert result["current_price"] == 150.00
        assert result["previous_close"] == 148.00
        assert result["change"] == 2.00
        assert result["change_percent"] == 1.35
        assert result["volume"] == 50000000
        assert result["market_cap"] == 2500000000000

    @patch("stock_data_tool.yf.Ticker")
    def test_get_stock_price_fallback_regular_market_price(self, mock_ticker):
        """Test fallback to regularMarketPrice when currentPrice not available"""
        mock_info = {
            "regularMarketPrice": 150.00,
            "previousClose": 148.00,
        }
        mock_ticker.return_value.info = mock_info

        result = get_stock_price.func("AAPL")

        assert result["current_price"] == 150.00

    @patch("stock_data_tool.yf.Ticker")
    def test_get_stock_price_error_handling(self, mock_ticker):
        """Test error handling for invalid ticker"""
        mock_ticker.side_effect = Exception("Invalid ticker")

        result = get_stock_price.func("INVALID")

        assert "error" in result
        assert "Invalid ticker" in result["error"]


class TestGetHistoricalPrices:
    """Tests for get_historical_prices tool"""

    @patch("stock_data_tool.yf.Ticker")
    def test_get_historical_prices_success(self, mock_ticker):
        """Test successful historical price retrieval"""
        # Create mock DataFrame
        dates = pd.date_range(end=datetime.now(), periods=90)
        mock_df = pd.DataFrame(
            {
                "Open": [150.0] * 90,
                "High": [155.0] * 90,
                "Low": [145.0] * 90,
                "Close": [150.0 + i * 0.5 for i in range(90)],
                "Volume": [50000000] * 90,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = get_historical_prices.func("AAPL", days=90)

        assert result["ticker"] == "AAPL"
        assert result["data_points"] == 90
        assert result["period"] == "90 days"
        assert "latest_close" in result
        assert "period_high" in result
        assert "period_low" in result
        assert "total_return" in result
        assert "volatility" in result
        assert len(result["prices"]) == 30  # Last 30 data points

    @patch("stock_data_tool.yf.Ticker")
    def test_get_historical_prices_empty_data(self, mock_ticker):
        """Test handling of empty data"""
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        result = get_historical_prices.func("INVALID")

        assert "error" in result
        assert "No data available" in result["error"]

    @patch("stock_data_tool.yf.Ticker")
    def test_get_historical_prices_custom_interval(self, mock_ticker):
        """Test with custom interval"""
        dates = pd.date_range(end=datetime.now(), periods=30, freq="h")
        mock_df = pd.DataFrame(
            {
                "Close": [150.0] * 30,
                "High": [155.0] * 30,
                "Low": [145.0] * 30,
                "Volume": [1000000] * 30,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = get_historical_prices.func("AAPL", days=1, interval="1h")

        assert result["ticker"] == "AAPL"
        assert result["data_points"] == 30


class TestGetStockFundamentals:
    """Tests for get_stock_fundamentals tool"""

    @patch("stock_data_tool.yf.Ticker")
    def test_get_stock_fundamentals_success(self, mock_ticker):
        """Test successful fundamentals retrieval"""
        mock_info = {
            "longName": "Apple Inc.",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "trailingPE": 25.5,
            "forwardPE": 22.3,
            "pegRatio": 1.8,
            "priceToBook": 35.2,
            "priceToSalesTrailing12Months": 7.5,
            "trailingEps": 6.15,
            "dividendYield": 0.005,
            "beta": 1.2,
            "profitMargins": 0.25,
            "revenueGrowth": 0.08,
            "recommendationKey": "buy",
        }
        mock_ticker.return_value.info = mock_info

        result = get_stock_fundamentals.func("AAPL")

        assert result["ticker"] == "AAPL"
        assert result["company_name"] == "Apple Inc."
        assert result["sector"] == "Technology"
        assert result["pe_ratio"] == 25.5
        assert result["recommendation"] == "buy"

    @patch("stock_data_tool.yf.Ticker")
    def test_get_stock_fundamentals_missing_fields(self, mock_ticker):
        """Test handling of missing fields"""
        mock_info = {"longName": "Test Company"}
        mock_ticker.return_value.info = mock_info

        result = get_stock_fundamentals.func("TEST")

        assert result["company_name"] == "Test Company"
        assert result["pe_ratio"] is None


class TestGetMultipleStocks:
    """Tests for get_multiple_stocks tool"""

    @patch("stock_data_tool.yf.Ticker")
    def test_get_multiple_stocks_success(self, mock_ticker):
        """Test successful multiple stocks retrieval"""

        def mock_ticker_side_effect(ticker):
            mock = Mock()
            if ticker == "AAPL":
                mock.info = {
                    "currentPrice": 150.00,
                    "regularMarketChangePercent": 1.5,
                    "volume": 50000000,
                    "marketCap": 2500000000000,
                }
            elif ticker == "MSFT":
                mock.info = {
                    "currentPrice": 300.00,
                    "regularMarketChangePercent": -0.5,
                    "volume": 30000000,
                    "marketCap": 2200000000000,
                }
            return mock

        mock_ticker.side_effect = mock_ticker_side_effect

        result = get_multiple_stocks.func(["AAPL", "MSFT"])

        assert "AAPL" in result
        assert "MSFT" in result
        assert result["AAPL"]["current_price"] == 150.00
        assert result["MSFT"]["current_price"] == 300.00

    @patch("stock_data_tool.yf.Ticker")
    def test_get_multiple_stocks_partial_error(self, mock_ticker):
        """Test handling of partial errors"""

        def mock_ticker_side_effect(ticker):
            mock = Mock()
            if ticker == "AAPL":
                mock.info = {
                    "currentPrice": 150.00,
                    "regularMarketChangePercent": 1.5,
                    "volume": 50000000,
                    "marketCap": 2500000000000,
                }
            else:
                raise Exception("Invalid ticker")
            return mock

        mock_ticker.side_effect = mock_ticker_side_effect

        result = get_multiple_stocks.func(["AAPL", "INVALID"])

        assert "AAPL" in result
        assert "INVALID" in result
        assert "current_price" in result["AAPL"]
        assert "error" in result["INVALID"]


class TestCalculatePortfolioValue:
    """Tests for calculate_portfolio_value tool"""

    @patch("stock_data_tool.yf.Ticker")
    def test_calculate_portfolio_value_success(self, mock_ticker):
        """Test successful portfolio value calculation"""

        def mock_ticker_side_effect(ticker):
            mock = Mock()
            prices = {"AAPL": 150.00, "MSFT": 300.00, "GOOGL": 2500.00}
            mock.info = {"currentPrice": prices.get(ticker, 0)}
            return mock

        mock_ticker.side_effect = mock_ticker_side_effect

        portfolio = {"AAPL": 10, "MSFT": 5, "GOOGL": 2}
        result = calculate_portfolio_value.func(portfolio)

        # Expected: AAPL: 10*150=1500, MSFT: 5*300=1500, GOOGL: 2*2500=5000
        # Total: 8000
        assert result["total_value"] == 8000
        assert result["num_positions"] == 3
        assert "holdings" in result
        assert result["holdings"]["AAPL"]["shares"] == 10
        assert result["holdings"]["AAPL"]["value"] == 1500
        assert abs(result["holdings"]["AAPL"]["weight"] - 18.75) < 0.01

    @patch("stock_data_tool.yf.Ticker")
    def test_calculate_portfolio_value_empty_portfolio(self, mock_ticker):
        """Test with empty portfolio"""
        result = calculate_portfolio_value.func({})

        assert result["total_value"] == 0
        assert result["num_positions"] == 0
        assert len(result["holdings"]) == 0

    @patch("stock_data_tool.yf.Ticker")
    def test_calculate_portfolio_value_fallback_price(self, mock_ticker):
        """Test fallback to regularMarketPrice"""

        def mock_ticker_side_effect(ticker):
            mock = Mock()
            mock.info = {"regularMarketPrice": 150.00}
            return mock

        mock_ticker.side_effect = mock_ticker_side_effect

        portfolio = {"AAPL": 10}
        result = calculate_portfolio_value.func(portfolio)

        assert result["total_value"] == 1500


# Integration test marker
@pytest.mark.integration
class TestStockDataToolIntegration:
    """Integration tests that make real API calls (use sparingly)"""

    def test_real_api_call_aapl(self):
        """Test real API call for AAPL (requires internet)"""
        result = get_stock_price.func("AAPL")

        assert "ticker" in result
        assert result["ticker"] == "AAPL"
        # Should have either current_price or error
        assert "current_price" in result or "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

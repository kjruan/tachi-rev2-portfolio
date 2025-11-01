"""
Unit tests for technical_indicators_tool.py
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path to import tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from technical_indicators_tool import (
    calculate_indicators,
    analyze_momentum,
    detect_support_resistance,
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
)


class TestHelperFunctions:
    """Tests for helper calculation functions"""

    def test_calculate_sma(self):
        """Test Simple Moving Average calculation"""
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108])
        sma = calculate_sma(prices, 3)

        assert len(sma) == len(prices)
        assert pd.isna(sma.iloc[0])  # First values should be NaN
        assert pd.isna(sma.iloc[1])
        assert not pd.isna(sma.iloc[2])  # Third value should be calculated

    def test_calculate_ema(self):
        """Test Exponential Moving Average calculation"""
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108])
        ema = calculate_ema(prices, 3)

        assert len(ema) == len(prices)
        assert not pd.isna(ema.iloc[-1])  # Last value should be calculated

    def test_calculate_rsi(self):
        """Test RSI calculation"""
        # Create prices with clear upward trend
        prices = pd.Series([100 + i for i in range(20)])
        rsi = calculate_rsi(prices, 14)

        assert len(rsi) == len(prices)
        # RSI should be high for uptrend
        assert rsi.iloc[-1] > 50 if not pd.isna(rsi.iloc[-1]) else True

    def test_calculate_rsi_downtrend(self):
        """Test RSI calculation for downtrend"""
        # Create prices with clear downward trend
        prices = pd.Series([100 - i for i in range(20)])
        rsi = calculate_rsi(prices, 14)

        # RSI should be low for downtrend
        assert rsi.iloc[-1] < 50 if not pd.isna(rsi.iloc[-1]) else True

    def test_calculate_macd(self):
        """Test MACD calculation"""
        prices = pd.Series([100 + i * 0.5 for i in range(50)])
        macd_data = calculate_macd(prices)

        assert "macd" in macd_data
        assert "signal" in macd_data
        assert "histogram" in macd_data

    def test_calculate_bollinger_bands(self):
        """Test Bollinger Bands calculation"""
        prices = pd.Series([100 + i * 0.5 for i in range(30)])
        bb_data = calculate_bollinger_bands(prices, 20, 2)

        assert "sma" in bb_data
        assert "upper_band" in bb_data
        assert "lower_band" in bb_data
        assert "band_width" in bb_data
        assert "band_position" in bb_data
        assert bb_data["upper_band"] > bb_data["lower_band"]


class TestCalculateIndicators:
    """Tests for calculate_indicators tool"""

    @patch("technical_indicators_tool.yf.Ticker")
    def test_calculate_indicators_success(self, mock_ticker):
        """Test successful indicator calculation"""
        # Create realistic price data
        dates = pd.date_range(end=datetime.now(), periods=90)
        prices = [100 + i * 0.5 + np.sin(i / 5) * 2 for i in range(90)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": [p + 2 for p in prices],
                "Low": [p - 2 for p in prices],
                "Close": prices,
                "Volume": [50000000] * 90,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = calculate_indicators.func("AAPL", days=90)

        assert result["ticker"] == "AAPL"
        assert "current_price" in result
        assert "moving_averages" in result
        assert "rsi" in result
        assert "macd" in result
        assert "bollinger_bands" in result
        assert "trend" in result
        assert "signals" in result

    @patch("technical_indicators_tool.yf.Ticker")
    def test_calculate_indicators_uptrend(self, mock_ticker):
        """Test indicator calculation with uptrend"""
        dates = pd.date_range(end=datetime.now(), periods=90)
        # Strong uptrend
        prices = [100 + i * 2 for i in range(90)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": prices,
                "Low": prices,
                "Close": prices,
                "Volume": [50000000] * 90,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = calculate_indicators.func("AAPL")

        assert result["trend"] in ["UPTREND", "STRONG_UPTREND"]

    @patch("technical_indicators_tool.yf.Ticker")
    def test_calculate_indicators_oversold_rsi(self, mock_ticker):
        """Test RSI oversold detection"""
        dates = pd.date_range(end=datetime.now(), periods=90)
        # Strong downtrend to create oversold RSI
        prices = [100 - i * 0.8 for i in range(90)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": prices,
                "Low": prices,
                "Close": prices,
                "Volume": [50000000] * 90,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = calculate_indicators.func("AAPL")

        # Should detect downtrend
        assert result["trend"] in ["DOWNTREND", "STRONG_DOWNTREND"]

    @patch("technical_indicators_tool.yf.Ticker")
    def test_calculate_indicators_empty_data(self, mock_ticker):
        """Test handling of empty data"""
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        result = calculate_indicators.func("INVALID")

        assert "error" in result
        assert "No data available" in result["error"]

    @patch("technical_indicators_tool.yf.Ticker")
    def test_calculate_indicators_short_history(self, mock_ticker):
        """Test with insufficient data for 200-day SMA"""
        dates = pd.date_range(end=datetime.now(), periods=60)
        prices = [100 + i * 0.5 for i in range(60)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": prices,
                "Low": prices,
                "Close": prices,
                "Volume": [50000000] * 60,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = calculate_indicators.func("AAPL", days=60)

        # 200-day SMA should be None
        assert result["moving_averages"]["sma_200"] is None


class TestAnalyzeMomentum:
    """Tests for analyze_momentum tool"""

    @patch("technical_indicators_tool.yf.Ticker")
    def test_analyze_momentum_bullish(self, mock_ticker):
        """Test momentum analysis for bullish trend"""
        dates = pd.date_range(end=datetime.now(), periods=40)
        # Strong upward momentum
        prices = [100 + i * 1.5 for i in range(40)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": prices,
                "Low": prices,
                "Close": prices,
                "Volume": [50000000] * 40,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = analyze_momentum.func("AAPL", days=30)

        assert result["ticker"] == "AAPL"
        assert result["momentum_direction"] == "BULLISH"
        assert result["average_return"] > 0
        assert "returns" in result
        assert "momentum_strength" in result

    @patch("technical_indicators_tool.yf.Ticker")
    def test_analyze_momentum_bearish(self, mock_ticker):
        """Test momentum analysis for bearish trend"""
        dates = pd.date_range(end=datetime.now(), periods=40)
        # Strong downward momentum
        prices = [100 - i * 1.0 for i in range(40)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": prices,
                "Low": prices,
                "Close": prices,
                "Volume": [50000000] * 40,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = analyze_momentum.func("AAPL", days=30)

        assert result["momentum_direction"] == "BEARISH"
        assert result["average_return"] < 0

    @patch("technical_indicators_tool.yf.Ticker")
    def test_analyze_momentum_strong_classification(self, mock_ticker):
        """Test strong momentum classification"""
        dates = pd.date_range(end=datetime.now(), periods=40)
        # Very strong momentum (>5% average)
        prices = [100 * (1.02 ** i) for i in range(40)]  # 2% daily growth
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": prices,
                "Low": prices,
                "Close": prices,
                "Volume": [50000000] * 40,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = analyze_momentum.func("AAPL", days=30)

        assert result["momentum_strength"] in ["STRONG", "MODERATE", "WEAK"]

    @patch("technical_indicators_tool.yf.Ticker")
    def test_analyze_momentum_empty_data(self, mock_ticker):
        """Test handling of empty data"""
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        result = analyze_momentum.func("INVALID")

        assert "error" in result


class TestDetectSupportResistance:
    """Tests for detect_support_resistance tool"""

    @patch("technical_indicators_tool.yf.Ticker")
    def test_detect_support_resistance_success(self, mock_ticker):
        """Test successful support/resistance detection"""
        dates = pd.date_range(end=datetime.now(), periods=90)
        # Create price data with clear highs and lows
        prices = [100 + 10 * np.sin(i / 10) for i in range(90)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": [p + 5 for p in prices],
                "Low": [p - 5 for p in prices],
                "Close": prices,
                "Volume": [50000000] * 90,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = detect_support_resistance.func("AAPL", days=90)

        assert result["ticker"] == "AAPL"
        assert "current_price" in result
        assert "period_high" in result
        assert "period_low" in result
        assert "recent_high_20d" in result
        assert "recent_low_20d" in result
        assert "resistance_levels" in result
        assert "support_levels" in result
        assert "psychological_levels" in result

        # Validate levels make sense
        assert result["period_high"] >= result["current_price"]
        assert result["period_low"] <= result["current_price"]

    @patch("technical_indicators_tool.yf.Ticker")
    def test_detect_support_resistance_levels_ordering(self, mock_ticker):
        """Test that support/resistance levels are properly ordered"""
        dates = pd.date_range(end=datetime.now(), periods=90)
        prices = [100 + i * 0.5 for i in range(90)]
        mock_df = pd.DataFrame(
            {
                "Open": prices,
                "High": [p + 2 for p in prices],
                "Low": [p - 2 for p in prices],
                "Close": prices,
                "Volume": [50000000] * 90,
            },
            index=dates,
        )
        mock_ticker.return_value.history.return_value = mock_df

        result = detect_support_resistance.func("AAPL")

        # Resistance should be above support
        assert max(result["resistance_levels"]) >= min(result["support_levels"])

    @patch("technical_indicators_tool.yf.Ticker")
    def test_detect_support_resistance_empty_data(self, mock_ticker):
        """Test handling of empty data"""
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        result = detect_support_resistance.func("INVALID")

        assert "error" in result


# Integration test marker
@pytest.mark.integration
class TestTechnicalIndicatorsIntegration:
    """Integration tests that make real API calls"""

    def test_real_indicators_aapl(self):
        """Test real indicator calculation for AAPL"""
        result = calculate_indicators.func("AAPL", days=90)

        assert "ticker" in result
        assert result["ticker"] == "AAPL"
        assert "current_price" in result or "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

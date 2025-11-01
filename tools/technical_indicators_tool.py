"""
Technical Indicators Tool for calculating various technical analysis metrics
"""

from crewai.tools import tool
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional


def calculate_sma(prices: pd.Series, period: int) -> pd.Series:
    """Calculate Simple Moving Average"""
    return prices.rolling(window=period).mean()


def calculate_ema(prices: pd.Series, period: int) -> pd.Series:
    """Calculate Exponential Moving Average"""
    return prices.ewm(span=period, adjust=False).mean()


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """Calculate MACD (Moving Average Convergence Divergence)"""
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line

    return {
        "macd": macd_line.iloc[-1] if not macd_line.empty else None,
        "signal": signal_line.iloc[-1] if not signal_line.empty else None,
        "histogram": histogram.iloc[-1] if not histogram.empty else None,
    }


def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: int = 2) -> Dict:
    """Calculate Bollinger Bands"""
    sma = calculate_sma(prices, period)
    std = prices.rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)

    current_price = prices.iloc[-1]
    current_sma = sma.iloc[-1]
    current_upper = upper_band.iloc[-1]
    current_lower = lower_band.iloc[-1]

    # Calculate position within bands (0 = lower band, 1 = upper band)
    band_position = (current_price - current_lower) / (current_upper - current_lower) if (current_upper - current_lower) != 0 else 0.5

    return {
        "sma": current_sma,
        "upper_band": current_upper,
        "lower_band": current_lower,
        "band_width": current_upper - current_lower,
        "band_position": band_position,
        "price": current_price,
    }


@tool("Calculate Technical Indicators")
def calculate_indicators(ticker: str, days: int = 90) -> Dict:
    """
    Calculate comprehensive technical indicators for a stock.

    Args:
        ticker: Stock ticker symbol
        days: Number of days of historical data to analyze (default: 90)

    Returns:
        Dictionary with various technical indicators
    """
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            return {"error": f"No data available for {ticker}"}

        prices = df["Close"]

        # Calculate indicators
        sma_20 = calculate_sma(prices, 20).iloc[-1]
        sma_50 = calculate_sma(prices, 50).iloc[-1]
        sma_200 = calculate_sma(prices, 200).iloc[-1] if len(prices) >= 200 else None

        ema_20 = calculate_ema(prices, 20).iloc[-1]
        ema_50 = calculate_ema(prices, 50).iloc[-1]

        rsi = calculate_rsi(prices).iloc[-1]
        macd_data = calculate_macd(prices)
        bb_data = calculate_bollinger_bands(prices)

        # Determine trend
        current_price = prices.iloc[-1]
        trend = "NEUTRAL"
        if sma_50:
            if current_price > sma_50 > sma_20:
                trend = "STRONG_UPTREND"
            elif current_price > sma_50:
                trend = "UPTREND"
            elif current_price < sma_50 < sma_20:
                trend = "STRONG_DOWNTREND"
            elif current_price < sma_50:
                trend = "DOWNTREND"

        # RSI analysis
        rsi_signal = "NEUTRAL"
        if rsi < 30:
            rsi_signal = "OVERSOLD"
        elif rsi > 70:
            rsi_signal = "OVERBOUGHT"
        elif 40 <= rsi <= 60:
            rsi_signal = "NEUTRAL"

        # MACD signal
        macd_signal = "NEUTRAL"
        if macd_data["macd"] and macd_data["signal"]:
            if macd_data["macd"] > macd_data["signal"] and macd_data["histogram"] > 0:
                macd_signal = "BULLISH"
            elif macd_data["macd"] < macd_data["signal"] and macd_data["histogram"] < 0:
                macd_signal = "BEARISH"

        return {
            "ticker": ticker,
            "current_price": float(current_price),
            "moving_averages": {
                "sma_20": float(sma_20) if sma_20 else None,
                "sma_50": float(sma_50) if sma_50 else None,
                "sma_200": float(sma_200) if sma_200 else None,
                "ema_20": float(ema_20) if ema_20 else None,
                "ema_50": float(ema_50) if ema_50 else None,
            },
            "rsi": {
                "value": float(rsi) if not pd.isna(rsi) else None,
                "signal": rsi_signal,
            },
            "macd": {
                **macd_data,
                "signal_interpretation": macd_signal,
            },
            "bollinger_bands": bb_data,
            "trend": trend,
            "signals": {
                "overall": macd_signal if macd_signal != "NEUTRAL" else rsi_signal,
                "rsi": rsi_signal,
                "macd": macd_signal,
                "trend": trend,
            },
        }

    except Exception as e:
        return {"error": f"Failed to calculate indicators for {ticker}: {str(e)}"}


@tool("Analyze Momentum")
def analyze_momentum(ticker: str, days: int = 30) -> Dict:
    """
    Analyze price momentum over different timeframes.

    Args:
        ticker: Stock ticker symbol
        days: Number of days to analyze (default: 30)

    Returns:
        Dictionary with momentum metrics
    """
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            return {"error": f"No data available for {ticker}"}

        prices = df["Close"]
        current_price = prices.iloc[-1]

        # Calculate returns over different periods
        returns = {}
        periods = [1, 5, 10, 20, 30]

        for period in periods:
            if len(prices) > period:
                past_price = prices.iloc[-period - 1]
                return_pct = ((current_price - past_price) / past_price) * 100
                returns[f"{period}d"] = float(return_pct)

        # Calculate momentum strength
        avg_return = np.mean(list(returns.values()))
        momentum_strength = "WEAK"
        if abs(avg_return) > 5:
            momentum_strength = "STRONG"
        elif abs(avg_return) > 2:
            momentum_strength = "MODERATE"

        momentum_direction = "BULLISH" if avg_return > 0 else "BEARISH" if avg_return < 0 else "NEUTRAL"

        return {
            "ticker": ticker,
            "current_price": float(current_price),
            "returns": returns,
            "average_return": float(avg_return),
            "momentum_strength": momentum_strength,
            "momentum_direction": momentum_direction,
        }

    except Exception as e:
        return {"error": f"Failed to analyze momentum for {ticker}: {str(e)}"}


@tool("Detect Support and Resistance")
def detect_support_resistance(ticker: str, days: int = 90) -> Dict:
    """
    Detect potential support and resistance levels.

    Args:
        ticker: Stock ticker symbol
        days: Number of days to analyze (default: 90)

    Returns:
        Dictionary with support and resistance levels
    """
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            return {"error": f"No data available for {ticker}"}

        # Simple support/resistance detection using local minima/maxima
        highs = df["High"]
        lows = df["Low"]
        current_price = df["Close"].iloc[-1]

        # Find recent high and low
        period_high = highs.max()
        period_low = lows.min()

        # Recent 20-day high/low
        recent_high = highs.tail(20).max()
        recent_low = lows.tail(20).min()

        # Calculate psychological levels (round numbers)
        psychological_levels = [
            round(current_price / 10) * 10,
            round(current_price / 5) * 5,
        ]

        return {
            "ticker": ticker,
            "current_price": float(current_price),
            "period_high": float(period_high),
            "period_low": float(period_low),
            "recent_high_20d": float(recent_high),
            "recent_low_20d": float(recent_low),
            "resistance_levels": [float(period_high), float(recent_high)],
            "support_levels": [float(period_low), float(recent_low)],
            "psychological_levels": psychological_levels,
        }

    except Exception as e:
        return {"error": f"Failed to detect support/resistance for {ticker}: {str(e)}"}


# Export all tools
__all__ = [
    "calculate_indicators",
    "analyze_momentum",
    "detect_support_resistance",
]

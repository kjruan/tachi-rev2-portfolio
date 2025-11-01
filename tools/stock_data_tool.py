"""
Stock Data Tool for fetching market data using yfinance
"""

from crewai.tools import tool
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional, List


@tool("Get Stock Price")
def get_stock_price(ticker: str) -> Dict:
    """
    Fetch current stock price and basic info for a given ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary with current price, change, volume, and market cap
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "ticker": ticker,
            "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
            "previous_close": info.get("previousClose"),
            "change": info.get("regularMarketChange"),
            "change_percent": info.get("regularMarketChangePercent"),
            "volume": info.get("volume"),
            "market_cap": info.get("marketCap"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
        }
    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}


@tool("Get Historical Prices")
def get_historical_prices(
    ticker: str, days: int = 90, interval: str = "1d"
) -> Dict:
    """
    Fetch historical price data for a stock.

    Args:
        ticker: Stock ticker symbol
        days: Number of days of historical data (default: 90)
        interval: Data interval ('1d', '1h', '5m', etc.) (default: '1d')

    Returns:
        Dictionary with historical OHLCV data and summary statistics
    """
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        df = stock.history(start=start_date, end=end_date, interval=interval)

        if df.empty:
            return {"error": f"No data available for {ticker}"}

        return {
            "ticker": ticker,
            "period": f"{days} days",
            "data_points": len(df),
            "start_date": df.index[0].strftime("%Y-%m-%d"),
            "end_date": df.index[-1].strftime("%Y-%m-%d"),
            "latest_close": float(df["Close"].iloc[-1]),
            "period_high": float(df["High"].max()),
            "period_low": float(df["Low"].min()),
            "avg_volume": int(df["Volume"].mean()),
            "total_return": float((df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100),
            "volatility": float(df["Close"].pct_change().std() * 100),
            "prices": df["Close"].tolist()[-30:],  # Last 30 data points
        }
    except Exception as e:
        return {"error": f"Failed to fetch historical data for {ticker}: {str(e)}"}


@tool("Get Stock Fundamentals")
def get_stock_fundamentals(ticker: str) -> Dict:
    """
    Fetch fundamental data for a stock including P/E, EPS, dividend yield, etc.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary with fundamental metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "ticker": ticker,
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "eps": info.get("trailingEps"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "profit_margin": info.get("profitMargins"),
            "revenue_growth": info.get("revenueGrowth"),
            "recommendation": info.get("recommendationKey", "N/A"),
        }
    except Exception as e:
        return {"error": f"Failed to fetch fundamentals for {ticker}: {str(e)}"}


@tool("Get Multiple Stocks")
def get_multiple_stocks(tickers: List[str]) -> Dict:
    """
    Fetch current data for multiple stocks at once.

    Args:
        tickers: List of ticker symbols

    Returns:
        Dictionary with data for each ticker
    """
    results = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            results[ticker] = {
                "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
                "change_percent": info.get("regularMarketChangePercent"),
                "volume": info.get("volume"),
                "market_cap": info.get("marketCap"),
            }
        except Exception as e:
            results[ticker] = {"error": str(e)}

    return results


@tool("Calculate Portfolio Value")
def calculate_portfolio_value(portfolio: Dict[str, float]) -> Dict:
    """
    Calculate total value of a portfolio.

    Args:
        portfolio: Dictionary mapping ticker symbols to number of shares
                  Example: {'AAPL': 10, 'MSFT': 15}

    Returns:
        Dictionary with portfolio value and breakdown
    """
    try:
        total_value = 0
        holdings = {}

        for ticker, shares in portfolio.items():
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("currentPrice", info.get("regularMarketPrice", 0))

            value = price * shares
            total_value += value

            holdings[ticker] = {
                "shares": shares,
                "price": price,
                "value": value,
                "weight": 0,  # Will calculate after total
            }

        # Calculate weights
        if total_value > 0:
            for ticker in holdings:
                holdings[ticker]["weight"] = (holdings[ticker]["value"] / total_value) * 100

        return {
            "total_value": total_value,
            "num_positions": len(portfolio),
            "holdings": holdings,
        }
    except Exception as e:
        return {"error": f"Failed to calculate portfolio value: {str(e)}"}


# Export all tools
__all__ = [
    "get_stock_price",
    "get_historical_prices",
    "get_stock_fundamentals",
    "get_multiple_stocks",
    "calculate_portfolio_value",
]

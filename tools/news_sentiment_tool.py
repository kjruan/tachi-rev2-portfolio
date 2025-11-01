"""
News and Sentiment Analysis Tool
Note: This is a simplified version. For production, integrate with:
- Financial news APIs (Finnhub, Alpha Vantage, NewsAPI)
- Social media sentiment (Twitter/X API)
- SEC filings
"""

from crewai.tools import tool
import yfinance as yf
from typing import Dict, List
from datetime import datetime, timedelta


@tool("Get Recent News")
def get_recent_news(ticker: str, max_items: int = 10) -> Dict:
    """
    Fetch recent news articles for a stock using yfinance.

    Args:
        ticker: Stock ticker symbol
        max_items: Maximum number of news items to return (default: 10)

    Returns:
        Dictionary with recent news articles
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news

        if not news:
            return {
                "ticker": ticker,
                "news_count": 0,
                "articles": [],
                "message": "No recent news available",
            }

        # Process news items
        articles = []
        for item in news[:max_items]:
            articles.append({
                "title": item.get("title", ""),
                "publisher": item.get("publisher", "Unknown"),
                "link": item.get("link", ""),
                "published": datetime.fromtimestamp(item.get("providerPublishTime", 0)).strftime("%Y-%m-%d %H:%M"),
                "type": item.get("type", "NEWS"),
            })

        # Simple sentiment heuristic based on keywords
        positive_keywords = ["rise", "gain", "profit", "growth", "beats", "exceeds", "strong", "bullish", "surge", "jump"]
        negative_keywords = ["fall", "loss", "decline", "weak", "miss", "warning", "bearish", "drop", "plunge", "crash"]

        sentiment_scores = []
        for article in articles:
            title_lower = article["title"].lower()
            pos_count = sum(1 for word in positive_keywords if word in title_lower)
            neg_count = sum(1 for word in negative_keywords if word in title_lower)

            if pos_count > neg_count:
                sentiment = "POSITIVE"
                score = 1
            elif neg_count > pos_count:
                sentiment = "NEGATIVE"
                score = -1
            else:
                sentiment = "NEUTRAL"
                score = 0

            article["sentiment"] = sentiment
            sentiment_scores.append(score)

        # Calculate overall sentiment
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        overall_sentiment = "POSITIVE" if avg_sentiment > 0.2 else "NEGATIVE" if avg_sentiment < -0.2 else "NEUTRAL"

        return {
            "ticker": ticker,
            "news_count": len(articles),
            "articles": articles,
            "overall_sentiment": overall_sentiment,
            "sentiment_score": round(avg_sentiment, 2),
        }

    except Exception as e:
        return {"error": f"Failed to fetch news for {ticker}: {str(e)}"}


@tool("Analyze Market Sentiment")
def analyze_market_sentiment(ticker: str) -> Dict:
    """
    Analyze overall market sentiment for a stock based on multiple factors.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary with sentiment analysis
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Analyst recommendations
        recommendation = info.get("recommendationKey", "").lower()
        rec_score = 0
        if "buy" in recommendation:
            rec_score = 2 if "strong" in recommendation else 1
        elif "sell" in recommendation:
            rec_score = -2 if "strong" in recommendation else -1

        # Price action
        current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
        fifty_day_avg = info.get("fiftyDayAverage", current_price)
        price_action_score = 1 if current_price > fifty_day_avg * 1.05 else -1 if current_price < fifty_day_avg * 0.95 else 0

        # Get news sentiment
        news_data = get_recent_news(ticker, max_items=5)
        news_score = news_data.get("sentiment_score", 0) if "error" not in news_data else 0

        # Combine scores
        total_score = (rec_score + price_action_score + news_score) / 3

        # Determine overall sentiment
        if total_score > 0.3:
            overall = "BULLISH"
        elif total_score < -0.3:
            overall = "BEARISH"
        else:
            overall = "NEUTRAL"

        return {
            "ticker": ticker,
            "overall_sentiment": overall,
            "sentiment_score": round(total_score, 2),
            "factors": {
                "analyst_recommendation": {
                    "value": recommendation,
                    "score": rec_score,
                },
                "price_action": {
                    "score": price_action_score,
                    "current_vs_50d_ma": round((current_price / fifty_day_avg - 1) * 100, 2) if fifty_day_avg else 0,
                },
                "news_sentiment": {
                    "score": news_score,
                    "article_count": news_data.get("news_count", 0),
                },
            },
            "recommendation": f"{overall} - Combined sentiment indicates {overall.lower()} outlook",
        }

    except Exception as e:
        return {"error": f"Failed to analyze sentiment for {ticker}: {str(e)}"}


@tool("Get Analyst Ratings")
def get_analyst_ratings(ticker: str) -> Dict:
    """
    Get analyst ratings and price targets for a stock.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary with analyst ratings and targets
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        current_price = info.get("currentPrice", info.get("regularMarketPrice"))
        target_high = info.get("targetHighPrice")
        target_low = info.get("targetLowPrice")
        target_mean = info.get("targetMeanPrice")
        target_median = info.get("targetMedianPrice")

        # Calculate upside/downside
        upside = ((target_mean - current_price) / current_price * 100) if target_mean and current_price else None

        return {
            "ticker": ticker,
            "current_price": current_price,
            "recommendation": info.get("recommendationKey", "N/A"),
            "num_analysts": info.get("numberOfAnalystOpinions"),
            "price_targets": {
                "high": target_high,
                "mean": target_mean,
                "median": target_median,
                "low": target_low,
            },
            "potential_upside": round(upside, 2) if upside else None,
            "recommendation_summary": info.get("recommendationKey", "N/A").upper(),
        }

    except Exception as e:
        return {"error": f"Failed to get analyst ratings for {ticker}: {str(e)}"}


# Export all tools
__all__ = [
    "get_recent_news",
    "analyze_market_sentiment",
    "get_analyst_ratings",
]

"""Market scanner - fetches candidate Polymarket markets for evaluation."""

import requests
from datetime import datetime, timedelta
import config

def fetch_markets():
    """
    Fetch active markets from Polymarket Gamma API.
    For v0: returns a hardcoded list for testing.
    For v1+: uncomment the API call below.
    """
    # Hardcoded test markets for initial testing
    test_markets = [
        {
            "market_id": "test_001",
            "title": "Will Bitcoin reach $100k by end of 2025?",
            "category": "Crypto",
            "resolution_date": "2025-12-31",
            "current_yes_price": 0.45,
            "current_no_price": 0.55,
            "liquidity_score": 15000
        },
        {
            "market_id": "test_002",
            "title": "Will there be a recession in Q1 2025?",
            "category": "Economics",
            "resolution_date": "2025-03-31",
            "current_yes_price": 0.30,
            "current_no_price": 0.70,
            "liquidity_score": 8000
        },
        {
            "market_id": "test_003",
            "title": "Will OpenAI release GPT-5 before June 2025?",
            "category": "Technology",
            "resolution_date": "2025-06-01",
            "current_yes_price": 0.25,
            "current_no_price": 0.75,
            "liquidity_score": 12000
        }
    ]
    
    return test_markets

# Uncomment below for real API integration later
# def fetch_markets_live():
#     """Fetch live markets from Polymarket API."""
#     url = f"{config.POLYMARKET_API_BASE}/markets"
#     params = {
#         "active": "true",
#         "closed": "false",
#         "_limit": 50
#     }
#     response = requests.get(url, params=params)
#     markets = response.json()
#     return [parse_market(m) for m in markets]

if __name__ == "__main__":
    markets = fetch_markets()
    print(f"Found {len(markets)} test markets")
    for m in markets:
        print(f"  - {m['title']}")

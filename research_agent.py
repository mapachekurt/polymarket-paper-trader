"""Research agent - enriches markets with edge estimates and thesis."""

import config

def enrich_market(market):
    """
    Enrich a market dict with:
    - model_edge: estimated edge based on price vs fair value
    - news_signal: placeholder for sentiment/news score
    - thesis: short text explaining the trade rationale
    
    For v0: uses simple heuristics.
    For v1+: integrate news API, LLM analysis, or historical data.
    """
    # Simple heuristic: if price is far from 50%, assume some edge
    yes_price = market.get("current_yes_price", 0.5)
    
    # Basic edge calculation (stub)
    # Real version would compare to research-based fair value
    if yes_price < 0.35:
        model_edge = 0.08  # 8% edge if very underpriced
    elif yes_price < 0.45:
        model_edge = 0.04  # 4% edge
    elif yes_price > 0.65:
        model_edge = 0.06  # 6% edge on NO side
    elif yes_price > 0.55:
        model_edge = 0.03  # 3% edge
    else:
        model_edge = 0.01  # minimal edge near 50/50
    
    # Add enriched fields
    market["model_edge"] = model_edge
    market["news_signal"] = "Neutral"  # Placeholder
    market["thesis"] = f"Edge based on price deviation from fair value"
    
    return market

if __name__ == "__main__":
    test_market = {
        "market_id": "test_001",
        "title": "Test market",
        "current_yes_price": 0.30
    }
    enriched = enrich_market(test_market)
    print(f"Enriched market: edge={enriched['model_edge']}, thesis={enriched['thesis']}")

"""Decision engine - converts research & edge into trade decisions."""

import config

def decide_trade(market, bankroll):
    """
    Given an enriched market and current bankroll, decide:
    - action: ENTER, SKIP, EXIT, HOLD
    - direction: YES or NO
    - size_dollars: how much to invest
    
    For v0: simple rules based on edge threshold.
    """
    model_edge = market.get("model_edge", 0)
    liquidity = market.get("liquidity_score", 0)
    
    # Filter 1: Liquidity check
    if liquidity < config.MIN_LIQUIDITY_SCORE:
        return {
            "action": "SKIP",
            "reason": "Insufficient liquidity",
            "direction": None,
            "size_dollars": 0
        }
    
    # Filter 2: Edge threshold
    if model_edge < config.MIN_EDGE_THRESHOLD:
        return {
            "action": "SKIP",
            "reason": f"Edge too low ({model_edge:.1%})",
            "direction": None,
            "size_dollars": 0
        }
    
    # Calculate position size
    # Kelly-inspired: size proportional to edge, capped by max risk
    raw_size = model_edge * bankroll
    capped_size = min(
        raw_size,
        config.MAX_RISK_PER_TRADE * bankroll,
        config.MAX_POSITION_SIZE * bankroll
    )
    
    # Determine direction based on YES price
    yes_price = market.get("current_yes_price", 0.5)
    direction = "YES" if yes_price < 0.5 else "NO"
    
    return {
        "action": "ENTER",
        "reason": f"Edge={model_edge:.1%}, liquidity OK",
        "direction": direction,
        "size_dollars": round(capped_size, 2)
    }

if __name__ == "__main__":
    test_market = {
        "market_id": "test_001",
        "title": "Test market",
        "current_yes_price": 0.30,
        "model_edge": 0.05,
        "liquidity_score": 10000
    }
    decision = decide_trade(test_market, config.BASE_BANKROLL)
    print(f"Decision: {decision}")

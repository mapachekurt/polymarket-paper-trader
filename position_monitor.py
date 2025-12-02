"""Position monitor - tracks open positions and calculates PnL."""

from datetime import datetime, timedelta
import config

def evaluate_positions(positions, current_prices):
    """
    Evaluate all open positions and determine exit actions.
    
    Args:
        positions: list of dicts with position info
        current_prices: dict mapping market_id to current_price
    
    Returns:
        list of (position, action) tuples where action is EXIT or HOLD
    """
    results = []
    
    for pos in positions:
        if pos["status"] != "OPEN":
            continue
            
        market_id = pos["market_id"]
        current_price = current_prices.get(market_id)
        
        if not current_price:
            results.append((pos, "HOLD", "No price data"))
            continue
        
        # Calculate PnL
        entry_price = pos["entry_price"]
        size_shares = pos["size_shares"]
        entry_value = pos["entry_value"]
        
        current_value = size_shares * current_price
        unrealized_pnl = current_value - entry_value
        pnl_pct = unrealized_pnl / entry_value if entry_value > 0 else 0
        
        # Update position dict
        pos["current_price"] = current_price
        pos["current_value"] = current_value
        pos["unrealized_pnl"] = unrealized_pnl
        
        # Exit conditions
        exit_reason = None
        
        # 1. Take profit
        if pnl_pct >= config.TAKE_PROFIT_PCT:
            exit_reason = "Take profit target hit"
        
        # 2. Stop loss
        elif pnl_pct <= -config.STOP_LOSS_PCT:
            exit_reason = "Stop loss triggered"
        
        # 3. Time exit
        elif "opened_at" in pos:
            opened = datetime.fromisoformat(pos["opened_at"])
            age_hours = (datetime.now() - opened).total_seconds() / 3600
            if age_hours > config.TIME_EXIT_HOURS:
                exit_reason = "Time exit (no movement)"
        
        if exit_reason:
            results.append((pos, "EXIT", exit_reason))
        else:
            results.append((pos, "HOLD", f"PnL: {pnl_pct:.1%}"))
    
    return results

if __name__ == "__main__":
    test_pos = [
        {
            "market_id": "test_001",
            "direction": "YES",
            "entry_price": 0.30,
            "size_shares": 100,
            "entry_value": 30,
            "status": "OPEN",
            "opened_at": "2025-12-01T10:00:00"
        }
    ]
    prices = {"test_001": 0.40}
    results = evaluate_positions(test_pos, prices)
    for pos, action, reason in results:
        print(f"{pos['market_id']}: {action} - {reason}")

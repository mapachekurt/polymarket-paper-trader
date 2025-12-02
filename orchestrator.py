"""Orchestrator - ties all modules together for daily scan."""

import json
import csv
from datetime import datetime
import market_scanner
import research_agent
import decision_engine
import config

def run_daily_scan():
    """
    Main orchestration function:
    1. Fetch markets from scanner
    2. Enrich each with research agent
    3. Run decision engine
    4. Output results as CSV
    """
    print(f"=== Polymarket Paper Trader - Daily Scan ===")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Bankroll: ${config.BASE_BANKROLL}\n")
    
    # Step 1: Fetch markets
    print("[1/3] Fetching markets...")
    markets = market_scanner.fetch_markets()
    print(f"Found {len(markets)} markets\n")
    
    # Step 2: Enrich with research
    print("[2/3] Running research agent...")
    enriched_markets = []
    for market in markets:
        enriched = research_agent.enrich_market(market.copy())
        enriched_markets.append(enriched)
    print(f"Enriched {len(enriched_markets)} markets\n")
    
    # Step 3: Run decision engine
    print("[3/3] Running decision engine...")
    results = []
    for market in enriched_markets:
        decision = decision_engine.decide_trade(market, config.BASE_BANKROLL)
        
        # Merge market + decision into output row
        output_row = {
            "market_id": market["market_id"],
            "title": market["title"],
            "category": market.get("category", "N/A"),
            "resolution_date": market.get("resolution_date", "N/A"),
            "current_yes_price": market["current_yes_price"],
            "liquidity_score": market.get("liquidity_score", 0),
            "model_edge": market["model_edge"],
            "recommended_action": decision["action"],
            "sizing_recommendation": decision["size_dollars"],
            "last_updated": datetime.now().isoformat()
        }
        results.append(output_row)
        
        print(f"  {market['title'][:50]}... -> {decision['action']} (${decision['size_dollars']})")
    
    # Step 4: Write CSV output
    output_file = "markets_output.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\n✓ Scan complete. Output written to {output_file}")
    return results

if __name__ == "__main__":
    results = run_daily_scan()

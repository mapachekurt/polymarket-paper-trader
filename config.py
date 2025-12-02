"""Configuration file for Polymarket paper trader."""

# Bankroll & Risk
BASE_BANKROLL = 10000  # $10k paper money
MAX_RISK_PER_TRADE = 0.02  # 2% of bankroll per trade
MAX_POSITION_SIZE = 0.10  # Max 10% of bankroll in a single position

# Edge & Entry Thresholds
MIN_EDGE_THRESHOLD = 0.03  # Minimum 3% edge to enter a trade
MIN_LIQUIDITY_SCORE = 5000  # Minimum liquidity (USD) to consider a market

# Exit Rules
TAKE_PROFIT_PCT = 0.20  # Exit at +20% profit
STOP_LOSS_PCT = 0.10  # Exit at -10% loss
TIME_EXIT_HOURS = 48  # Exit if no movement within 48 hours

# Polymarket API (Gamma/CLOB endpoints)
POLYMARKET_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"

# For later: API keys if needed for authenticated endpoints
API_KEY = None  # Not needed for read-only paper trading

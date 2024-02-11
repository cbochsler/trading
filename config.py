import alpaca_trade_api as tradeapi
from alpaca_trade_api import REST
from datetime import datetime, timedelta

API_KEY = 'PKF7JLDJYPD0AHQ98BUH'
API_SECRET = 'tMRQvLYJbndksM00QEX17YfTdxiOnW7sDZf6e6Uf'
BASE_URL = 'https://paper-api.alpaca.markets'  # paper trading URL for testing

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

symbol = 'AAPL'
timeframe = '1D'
end_date = datetime.today() - timedelta(days=1)
start_date = end_date - timedelta(days=365)
qty = 10  # Define your quantity based on your strategy or account size

short_window = 20  # Example short window size
long_window = 50  # Example long window size
import alpaca_trade_api as tradeapi
from alpaca_trade_api import REST

API_KEY = 'PKF7JLDJYPD0AHQ98BUH'
API_SECRET = 'tMRQvLYJbndksM00QEX17YfTdxiOnW7sDZf6e6Uf'
BASE_URL = 'https://paper-api.alpaca.markets'  # paper trading URL for testing

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

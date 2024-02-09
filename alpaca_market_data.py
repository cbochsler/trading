import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def get_historical_data(symbol, start_date, end_date, timeframe):
    """
    Fetch historical market data for a symbol.
    
    :param symbol: The stock symbol to fetch data for (e.g., 'AAPL').
    :param start_date: Start date for the data in 'YYYY-MM-DD' format.
    :param end_date: End date for the data in 'YYYY-MM-DD' format.
    :param timeframe: The timeframe for the data ('minute', 'day', etc.).
    :return: Dataframe containing the historical market data.
    """
    # barset = api.get_barset(symbol, timeframe, start=start_date, end=end_date)
    bars = api.get_bars(symbol, timeframe, start_date, end_date).df
    return bars

def get_real_time_data(symbol):
    """
    Fetch real-time price data for a symbol.
    
    :param symbol: The stock symbol to fetch data for (e.g., 'AAPL').
    :return: Current price data for the symbol.
    """
    # This uses the IEX exchange data for real-time prices
    quote = api.get_latest_trade(symbol)
    return quote

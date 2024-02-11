import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL
import requests
from time import sleep

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

def fetch_with_retry(url, headers, max_retries=5, backoff_factor=0.3):
    """
    Attempts to fetch data with retries on failure.
    
    :param url: URL to fetch data from.
    :param headers: Headers to include in the request.
    :param max_retries: Maximum number of retry attempts.
    :param backoff_factor: Factor to determine the delay between retries.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Handle specific HTTP errors if needed
            print(f"HTTPError: {e}")
        except requests.exceptions.RequestException as e:
            # Handle other request issues (e.g., connectivity)
            print(f"RequestException: {e}")
            sleep((2 ** attempt) * backoff_factor)
        else:
            break
    else:
        print("Max retries exceeded with no success.")
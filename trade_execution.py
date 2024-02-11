import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL
from time import sleep

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def handle_api_limit(response):
    """
    Checks if the response indicates an API limit has been reached and sleeps accordingly.
    
    :param response: The API response to check.
    """
    if response.status_code == 429:  # 429 is the HTTP status code for Too Many Requests
        retry_after = int(response.headers.get('Retry-After', 60))  # Default to 60 seconds if header is missing
        print(f"Rate limit reached. Cooling off for {retry_after} seconds.")
        sleep(retry_after)

def check_position(symbol):
    """
    Check if we currently hold a position in the specified symbol.
    
    :param symbol: Stock symbol
    :return: Position quantity (positive for long, negative for short, 0 for no position)
    """
    try:
        position = api.get_position(symbol)
        return int(position.qty)
    except Exception as e:
        # Assuming no position is held if an exception occurs
        return 0

def place_order(symbol, qty, side, order_type='market', time_in_force='gtc', retries=3):
    """
    Place an order through the Alpaca API.
    
    :param symbol: Stock symbol
    :param qty: Quantity of shares to buy/sell
    :param side: 'buy' or 'sell'
    :param order_type: Type of order, default is 'market'
    :param time_in_force: How long the order remains in effect, default is 'gtc' (good til canceled)
    """
    attempt = 0
    while attempt < retries:
        try:
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force
            )
            attempt += 1
            print(f"Successfully placed {side} order for {qty} shares of {symbol}.")
        except tradeapi.rest.APIError as e:  # Catching the APIError specifically
            error_message = str(e)
            if "wash trade" in error_message.lower():
                print("Failed to place order due to potential wash trade detection. Consider revising your strategy.")
            elif "rate limit" in str(e).lower():
                handle_api_limit(e.response)
            else:
                print(f"Error placing {side} order for {symbol} on attempt {attempt}: {error_message}")
                sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:  # A general exception for any other errors
            print(f"An unexpected error occurred when placing the order on attempt {attempt}: {e}")
            break  # Break on non-retriable errors

def execute_trade(signal, symbol, qty):
    """
    Executes a trade based on the given signal.
    
    :param signal: Trading signal ('buy' or 'sell')
    :param symbol: Stock symbol
    :param qty: Quantity of shares to trade
    """
    current_position = check_position(symbol)
    if signal == 'buy' and current_position >= 0:
        # Place a buy order if we don't have a short position
        place_order(symbol, qty, 'buy')
    elif signal == 'sell' and current_position <= 0:
        # If we have a short position, cover it
        place_order(symbol, abs(current_position), 'buy')
    else:
        # Place a sell order if we have a long position to sell
        place_order(symbol, qty, 'sell')

import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

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

def place_order(symbol, qty, side, order_type='market', time_in_force='gtc'):
    """
    Place an order through the Alpaca API.
    
    :param symbol: Stock symbol
    :param qty: Quantity of shares to buy/sell
    :param side: 'buy' or 'sell'
    :param order_type: Type of order, default is 'market'
    :param time_in_force: How long the order remains in effect, default is 'gtc' (good til canceled)
    """
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
        print(f"Successfully placed {side} order for {qty} shares of {symbol}.")
    except Exception as e:
        print(f"An error occurred when placing the order: {e}")

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
        # Only place a sell order if we have a position
        if current_position < 0:
            # If we have a short position, cover it
            place_order(symbol, abs(current_position), 'buy')
        else:
            # Place a sell order if we have a long position to sell
            place_order(symbol, qty, 'sell')

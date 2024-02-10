from alpaca_market_data import get_historical_data, get_real_time_data
from trade_execution import execute_trade
from trading_strategy import detect_crossover, calculate_sma
from datetime import datetime, timedelta

symbol = 'AAPL'
timeframe = '1D'
end_date = datetime.today() - timedelta(days=1)
start_date = end_date - timedelta(days=365)
qty = 10  # Define your quantity based on your strategy or account size

short_window = 20  # Example short window size
long_window = 50  # Example long window size

# Example: Fetch historical data for AAPL
historical_data = get_historical_data(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), timeframe)
print(historical_data)

# Example: Fetch real-time data for AAPL
real_time_data = get_real_time_data(symbol)
print(real_time_data)

# Assuming 'historical_data' is a DataFrame with a 'close' column
prices = historical_data['close'].values

short_sma = calculate_sma(prices, short_window)
long_sma = calculate_sma(prices, long_window)

signal, index = detect_crossover(short_sma, long_sma)

if signal == 'buy':
    print("Buy signal detected.")
elif signal == 'sell':
    print("Sell signal detected.")
else:
    print("No crossover detected.")

# Execute the trade
execute_trade(signal, symbol, qty)
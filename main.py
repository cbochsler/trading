from alpaca_market_data import get_historical_data, get_real_time_data
from trade_execution import execute_trade
from trading_strategy import detect_crossover, calculate_sma
from config import symbol, timeframe, end_date, start_date, qty, short_window, long_window
import logging
import sys
from time import sleep


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Commented while loop - not needed for the moment
    #while True:
        try:  
            # Example: Fetch historical data
            historical_data = get_historical_data(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), timeframe)
            print(historical_data)

            # Example: Fetch real-time data
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
            pass
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            # Decide on a cooldown period before retrying or exit
            sleep(60)  # Cooldown period of 60 seconds before retrying

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Shutdown requested...exiting")
    except Exception:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise


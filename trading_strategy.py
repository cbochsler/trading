import numpy as np

def calculate_sma(prices, window):
    """
    Calculate the simple moving average (SMA) for the given prices.
    
    :param prices: A list or array of prices.
    :param window: The window size for the SMA calculation.
    :return: A numpy array containing the SMA values.
    """
    sma = np.convolve(prices, np.ones(window), 'valid') / window
    return sma

def detect_crossover(short_sma, long_sma):
    """
    Detects a crossover between two SMA lines.
    
    :param short_sma: The short window SMA array.
    :param long_sma: The long window SMA array.
    :return: A tuple containing the crossover signal ('buy', 'sell', or None) and the index at which it occurred.
    """
    # Ensure both arrays are of the same length for comparison
    min_length = min(len(short_sma), len(long_sma))
    short_sma, long_sma = short_sma[-min_length:], long_sma[-min_length:]
    
    # Look for crossover
    crossover_point = None
    for i in range(1, min_length):
        if short_sma[i-1] < long_sma[i-1] and short_sma[i] > long_sma[i]:
            return ('buy', i)
        elif short_sma[i-1] > long_sma[i-1] and short_sma[i] < long_sma[i]:
            return ('sell', i)
    return (None, crossover_point)
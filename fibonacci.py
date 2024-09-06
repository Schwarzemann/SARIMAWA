def fibonacci_retracement(highest_price, lowest_price):
    # Calculate the price difference
    price_difference = highest_price - lowest_price
    
    # Calculate Fibonacci retracement levels
    fibonacci_levels = {
        0: highest_price,
        0.236: highest_price - 0.236 * price_difference,
        0.382: highest_price - 0.382 * price_difference,
        0.5: highest_price - 0.5 * price_difference,
        0.618: highest_price - 0.618 * price_difference,
        1: lowest_price
    }
    
    return fibonacci_levels

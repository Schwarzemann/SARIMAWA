import pandas as pd
import statsmodels.api as sm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_guess():
    try:
        # Load price data from CSV file
        df = pd.read_csv('realtime_data.csv', parse_dates=['timestamp'])
    except FileNotFoundError:
        # If the CSV file does not exist, return a default guess
        logger.warning("CSV file not found. Returning default guess.")
        return 0, pd.Timestamp.now()
    
    if df.empty:
        # If the DataFrame is empty, return a default guess
        logger.warning("DataFrame is empty. Returning default guess.")
        return 0, pd.Timestamp.now()
    
    # Ensure there are enough observations for the model
    min_observations = 24  # Example: Ensure at least 24 observations for hourly data
    if len(df) < min_observations:
        logger.warning(f"Not enough data points. Required: {min_observations}, available: {len(df)}. Returning default guess.")
        return 0, pd.Timestamp.now()

    # Set the timestamp column as the index
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)

    # Resample data to hourly frequency
    df_hourly = df['price'].resample('H').mean().ffill()

    logger.info("Training SARIMA model...")
    # Train SARIMA model
    model = sm.tsa.SARIMAX(df_hourly, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
    results = model.fit(disp=False)
    logger.info("Model training completed.")

    # Log the summary of the SARIMA model
    logger.info(results.summary())

    # Forecast future prices
    forecast_steps = 24  # Example: forecast next 24 hours
    forecast = results.get_forecast(steps=forecast_steps)
    forecast_values = forecast.predicted_mean

    logger.info(f"Forecast for next {forecast_steps} steps: {forecast_values}")

    # Estimate time to reach a specific price level
    target_price = 50000  # Example: target price
    
    for i, price in enumerate(forecast_values):
        if price >= target_price:
            # Found the time index where price crosses or exceeds the target price
            timestamp = df_hourly.index[-1] + pd.Timedelta(hours=i)
            return price, timestamp

    # If target price is not reached in the forecasted period, return the last forecasted price and timestamp
    return forecast_values[-1], df_hourly.index[-1] + pd.Timedelta(hours=forecast_steps)

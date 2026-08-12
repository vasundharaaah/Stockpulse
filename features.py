import pandas as pd


def check_price_alert(current_price, target_price, condition="above"):
    
    if current_price is None or target_price is None:
        return False, "Waiting for valid price data..."

    if condition == "above":
        if current_price >= target_price:
            return True, f"ALERT: Price is above {target_price}!"
    elif condition == "below":
        if current_price <= target_price:
            return True, f"ALERT: Price dropped below {target_price}!"
            
    
    return False, "Price within range."


def export_to_csv(data, ticker):
   
    if data is None or data.empty:
        return False, "No data available to export."

    try:
        filename = f"{ticker}_history.csv"
        data.to_csv(filename)
        return True, f" Data successfully exported to {filename}"
    
    except Exception as e:
        return False, f" Error saving file: {e}"


def get_app_instructions():

    return """
    ## 🛠️ StockPulse: User Guide
    
    ### 1. Ticker Search & Recognition
    * **Indian Markets:** Simply enter the symbol (e.g., `TCS`, `INFY`). The app automatically appends `.NS` to fetch data from the National Stock Exchange.

    ### 2. Technical Analysis Tools
    * **Candlestick Charts:** View Open, High, Low, and Close prices for any selected period.
    * **SMA (Moving Averages):** Toggle the **SMA** switch to see the 20-day (gold dot) and 50-day (blue dash) trend lines calculated from historical close prices.
    * **Volume Analysis:** Toggle **Volume** to see color-coded bars indicating buying (green) or selling (red) pressure.
    
    ### 3. Price Alerts & Monitoring
    * Navigate to **'Price Alerts'** to set a target price.
    * Choose **'Above'** or **'Below'** to set your condition.
    * The system checks the current price against your target and provides a status update: **TRIGGERED** or **MONITORING**.
    
    ### 4. Data Portability
    * Use the **'Export Data'** tab to fetch historical records for periods ranging from 1 month to 5 years.
    * Click **'Download CSV'** to save the OHLCV dataset directly to your computer.
    * Exported files are named using the format `TICKER_history.csv`.
    
    ### 5. Navigation & Shortcuts
    * Use the **Sidebar** to switch between lookup, alerts, and export tools.
    * Rapidly change chart ranges (1D, 1M, 1Y, etc.) using the **Segmented Control**.
    
    """
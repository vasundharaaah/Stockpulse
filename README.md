Description
StockPulse is a Streamlit-based dashboard for tracking stock prices in real time. It pulls live data from Yahoo Finance, lets you visualize price movement with moving averages and volume, set price alerts for tickers you're watching, and export historical data whenever you need it outside the app. Built with a dark, minimal UI so it's actually pleasant to leave open all day.

Features
Stock Lookup — search any ticker and see current price, day high/low, and volume at a glance. Indian tickers auto-append .NS, so TCS resolves to TCS.NS without extra typing.
Interactive Charts — price charts with optional SMA overlay and volume, switchable across 1D, 1W, 1M, 3M, 1Y, and 5Y timeframes.
Price Alerts — set a target price and a condition (above/below) and check whether it's been hit.
CSV Export — pull historical OHLCV data for any ticker and time range, preview it, and download it.
Standalone Charting — plotting.py runs independently of the dashboard for quick matplotlib charts (single stock, multi-stock comparison, multi-timeframe view).

Project Structure
├── app.py # Streamlit app — pages, layout, and styling 
├── backend.py # Data layer — fetches and formats stock data via yfinance 
├── features.py # Price alerts, CSV export, and in-app help text 
├── plotting.py # Standalone matplotlib charting utilities 
└── requirements.txt

How to Run
Clone the repo -- bash git clone https://github.com/<your-username>/stockpulse.git cd stockpulse
Install dependencies -- bash pip install streamlit plotly pandas yfinance matplotlib
Run the app -- bash streamlit run app.py -- Opens at `localhost:8501
(Optional) Run the standalone charts -- bash python plotting.py 

Tech Stack
Python
Streamlit — web app framework
yfinance — live stock data from Yahoo Finance
Plotly — interactive charts in the dashboard
Matplotlib — standalone charting
Pandas — data handling

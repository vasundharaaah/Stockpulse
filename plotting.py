# plotting.py — Member 3: Visualization Specialist

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance as yf


# ─────────────────────────────────────────────
# CORE FUNCTION: Fetch data for a given period
# ─────────────────────────────────────────────
def fetch_plot_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()


# ─────────────────────────────────────────────
# TECHNICAL INDICATOR: Simple Moving Average
# ─────────────────────────────────────────────
def add_sma(data, window=20):
    data = data.copy()
    col_name = f"SMA_{window}"
    data[col_name] = data["Close"].rolling(window=window).mean()
    return data


# ─────────────────────────────────────────────
# PLOT 1: Single Stock Line Chart + SMA
# ─────────────────────────────────────────────
def plot_single_stock(ticker, period="1mo", sma_window=20):
    data = fetch_plot_data(ticker, period)

    if data.empty:
        print(f"No data available for {ticker}.")
        return

    data = add_sma(data, window=sma_window)
    sma_col = f"SMA_{sma_window}"

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(data.index, data["Close"],
            label="Close Price", color="#1f77b4", linewidth=2)

    if data[sma_col].notna().sum() > 0:
        ax.plot(data.index, data[sma_col],
                label=f"SMA ({sma_window})",
                color="orange", linewidth=1.5, linestyle="--")

    ax.set_title(f"{ticker} — Price Chart ({period})",
                 fontsize=15, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (₹ / $)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# PLOT 2: Multiple Stocks Comparison Chart
# ─────────────────────────────────────────────
def plot_multiple_stocks(tickers, period="1mo"):
    fig, ax = plt.subplots(figsize=(13, 6))
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for i, ticker in enumerate(tickers):
        data = fetch_plot_data(ticker, period)
        if data.empty:
            print(f"Skipping {ticker} — no data.")
            continue

        normalized = (data["Close"] / data["Close"].iloc[0]) * 100
        ax.plot(data.index, normalized,
                label=ticker,
                color=colors[i % len(colors)], linewidth=2)

    ax.set_title(f"Stock Comparison — Normalized to 100 ({period})",
                 fontsize=15, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Relative Price (base = 100)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# PLOT 3: Timeframe View (1 Day, 1 Month, 1 Year)
# ─────────────────────────────────────────────
def plot_timeframe_view(ticker):
    periods = {"1 Day": "1d", "1 Month": "1mo", "1 Year": "1y"}

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(f"{ticker} — Multi-Timeframe View",
                 fontsize=16, fontweight="bold")

    for ax, (label, period) in zip(axes, periods.items()):
        data = fetch_plot_data(ticker, period)

        if data.empty:
            ax.set_title(f"{label} — No Data")
            continue

        window = min(20, max(2, len(data) // 2))
        data = add_sma(data, window=window)
        sma_col = [c for c in data.columns if c.startswith("SMA_")][0]

        ax.plot(data.index, data["Close"],
                color="#1f77b4", linewidth=1.8, label="Close")

        if data[sma_col].notna().sum() > 0:
            ax.plot(data.index, data[sma_col],
                    color="orange", linewidth=1.2,
                    linestyle="--", label="SMA")

        ax.set_title(label, fontsize=12)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# TEST — runs when you run this file directly
# ─────────────────────────────────────────────
if __name__ == "__main__":

    print("📈 Graph 1: Single Stock...")
    plot_single_stock("TCS.NS", period="1mo", sma_window=20)

    print("📊 Graph 2: Multiple Stocks Comparison...")
    plot_multiple_stocks(["TCS.NS", "INFY.NS", "RELIANCE.NS"], period="1mo")

    print("📉 Graph 3: Timeframe View...")
    plot_timeframe_view("TCS.NS")
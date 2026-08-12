import yfinance as yf


def format_ticker(ticker):
    ticker = ticker.strip().upper()

    if ticker.startswith("^"):
        return ticker

    if not ticker.endswith(".NS"):
        ticker += ".NS"

    return ticker


def fetch_stock_data(ticker, period="1mo"):
    try:
        ticker = format_ticker(ticker)
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)

        if data.empty:
            return None

        return data.dropna()

    except Exception:
        return None


def get_latest_price(data):
    if data is None or data.empty:
        return None

    latest = data.iloc[-1]

    return {
        "price": round(latest["Close"], 2),
        "high": round(latest["High"], 2),
        "low": round(latest["Low"], 2),
        "volume": int(latest["Volume"])
    }


def get_change_percent(data):
    if data is None or len(data) < 2:
        return None

    latest = data.iloc[-1]["Close"]
    prev = data.iloc[-2]["Close"]

    return round(((latest - prev) / prev) * 100, 2)


def process_multiple_stocks(tickers, period="1mo"):
    results = {}

    for ticker in tickers:
        data = fetch_stock_data(ticker, period)

        if data is not None:
            formatted_ticker = format_ticker(ticker)

            results[formatted_ticker] = {
                "data": data,
                "latest": get_latest_price(data),
                "change_percent": get_change_percent(data)
            }
        else:
            results[ticker] = None

    return results
import os
import tempfile
import yfinance as yf

# Set cache location to a clean temporary directory to avoid SQLite locks
yf.set_tz_cache_location(os.path.join(tempfile.gettempdir(), "yf_cache"))

def get_market_data(tickers, period="1y", start_date=None, end_date=None, **kwargs):
    """
    Fetch close prices and calculate mean returns (mu) and covariance matrix (sigma).
    Supports parameters from both CLI (period) and Streamlit Web UI (start_date, end_date).
    """
    # Download stock data using start/end dates if provided, else period
    if start_date and end_date:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=True)
    else:
        data = yf.download(tickers, period=period, progress=False, auto_adjust=True)

    # Handle multi-level or single DataFrame column outputs from yfinance
    if "Close" in data:
        df = data["Close"]
    elif "Adj Close" in data:
        df = data["Adj Close"]
    else:
        df = data

    # Clean missing values
    df = df.dropna(axis=1, how="all").ffill().bfill()

    # Calculate daily percentage returns
    returns = df.pct_change().dropna()

    # Annualized mean returns (mu) and covariance matrix (sigma)
    mu = returns.mean() * 252
    sigma = returns.cov() * 252

    asset_names = list(df.columns)

    return mu.values, sigma.values, asset_names

# Alias for backwards compatibility
fetch_stock_data = get_market_data
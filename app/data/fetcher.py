import yfinance as yf
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'cache')
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_data(ticker, start_date, end_date):
    cache_file = os.path.join(DATA_DIR, f"{ticker}_{start_date}_{end_date}.csv")
    
    if os.path.exists(cache_file):
        print(f"Loading {ticker} from cache")
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True, date_format='ISO8601', header=[0, 1])
        df.columns = df.columns.get_level_values(0)
        # Drop any rows where index is not a valid date
        df = df[pd.to_datetime(df.index, errors='coerce').notna()]
        return df
    
    print(f"Fetching {ticker} from Yahoo Finance")
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    
    if df.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    
    df.to_csv(cache_file)
    return df
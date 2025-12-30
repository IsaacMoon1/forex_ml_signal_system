import pandas as pd

def load_forex_data(path="data/eurusd.csv"):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time').reset_index(drop=True)
    return df

import ta

def add_features(df):
    df = df.copy()

    df['return'] = df['close'].pct_change()

    df['rsi_14'] = ta.momentum.RSIIndicator(
        df['close'], window=14
    ).rsi()

    atr = ta.volatility.AverageTrueRange(
        df['high'], df['low'], df['close'], window=14
    )
    df['atr_14'] = atr.average_true_range()

    df['sma_10'] = df['close'].rolling(10).mean()
    df['sma_20'] = df['close'].rolling(20).mean()

    df = df.dropna().reset_index(drop=True)
    return df

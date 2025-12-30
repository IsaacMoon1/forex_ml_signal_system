import numpy as np
import pandas as pd


def backtest(df, model, features, initial_balance=10_000):
    df = df.copy()

    # ============================
    # 1. MODEL CONFIDENCE SIGNALS
    # ============================
    proba = model.predict_proba(df[features])[:, 1]

    df['signal'] = 0
    df.loc[proba > 0.60, 'signal'] = 1
    df.loc[proba < 0.40, 'signal'] = -1

    # ============================
    # 2. POSITION MANAGEMENT
    # ============================
    position = 0
    entry_price = 0
    equity = initial_balance

    trades = []

    for i in range(1, len(df)):
        price = df.iloc[i]['close']
        signal = df.iloc[i]['signal']

        # ENTER trade
        if position == 0 and signal != 0:
            position = signal
            entry_price = price

        # EXIT trade
        elif position != 0 and signal == -position:
            pct_return = (price - entry_price) / entry_price
            trade_return = pct_return * position

            equity *= (1 + trade_return)

            trades.append(trade_return)

            position = 0
            entry_price = 0

    # ============================
    # 3. METRICS (TRADE-BASED)
    # ============================
    trades = np.array(trades)

    total_return = (equity / initial_balance - 1) * 100

    if len(trades) > 0:
        win_rate = (trades > 0).sum() / len(trades) * 100
    else:
        win_rate = 0.0

    return df, total_return, win_rate

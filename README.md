
---

## Data Source
Historical EUR/USD data is downloaded from Yahoo Finance using the `yfinance` library.

- Instrument: EUR/USD
- Timeframe: 1-hour candles
- Lookback: ~2 years (Yahoo Finance limit for intraday data)

The dataset is saved locally as a CSV file and reused consistently across the entire pipeline to avoid data leakage or inconsistencies.

---

## Feature Engineering
The following features are derived from price data:

- Returns (percentage change)
- Technical indicators (RSI, ATR, moving averages)
- Lagged price information

A binary classification target is created:
- `1` if the next candle closes higher than the current close
- `0` otherwise

---

## Model
A Random Forest classifier is used for signal prediction.

- The dataset is split chronologically (no shuffling)
- The model predicts directional movement (up or down)
- Accuracy is reported on an out-of-sample test set

Accuracy is used as a baseline metric and does not represent trading profitability on its own.

---

## Backtesting Logic
A simple backtesting framework evaluates predicted signals:

- Long-only trades based on model predictions
- Returns are calculated using price differences
- No leverage, position sizing, or transaction costs by default

The backtest is intentionally conservative to avoid misleading performance metrics.

---

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt

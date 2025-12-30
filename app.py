import streamlit as st
import pandas as pd

from src.features import add_features
from src.model import train_model
from src.backtest import backtest


# ============================
# APPLICATION CONFIGURATION
# ============================
st.set_page_config(
    page_title="Forex ML Signal and Backtesting System",
    layout="wide"
)

st.title("Forex Machine Learning Signal and Backtesting System")

st.markdown("""
### System Overview

This application presents a machine learning–based Forex trading research system.
It combines feature engineering, supervised learning, and a trade-level backtesting
engine designed to avoid common sources of overestimation and data leakage.

The objective of the system is not to predict every price movement, but to:
- Identify higher-probability directional opportunities
- Trade selectively using model confidence
- Evaluate performance using realistic, trade-based metrics
""")

st.divider()


# ============================
# DATA LOADING
# ============================
st.subheader("1. Load Market Data")

data_file = st.file_uploader(
    "Upload OHLC Forex CSV file (required columns: open, high, low, close)",
    type=["csv"]
)

if data_file is None:
    st.info("Please upload a Forex CSV file to continue.")
    st.stop()

df = pd.read_csv(data_file)
df.columns = df.columns.str.lower()

required_cols = {"open", "high", "low", "close"}
if not required_cols.issubset(df.columns):
    st.error(f"The uploaded CSV must contain the following columns: {required_cols}")
    st.stop()

st.write(f"Rows loaded: {len(df):,}")
st.dataframe(df.head())


# ============================
# FEATURE ENGINEERING
# ============================
st.subheader("2. Feature Engineering")

df_feat = add_features(df)

st.markdown("The following engineered features are used by the model:")
st.code([
    "return",
    "rsi_14",
    "atr_14",
    "sma_10",
    "sma_20"
])

st.dataframe(df_feat.head())


# ============================
# MODEL TRAINING
# ============================
st.subheader("3. Model Training")

with st.spinner("Training model on historical data..."):
    model, features, accuracy = train_model(df_feat)

st.metric("Out-of-Sample Accuracy", f"{accuracy:.2f}")

st.markdown("""
**Interpretation of Accuracy**

In financial time series, accuracy is not a sufficient measure of performance.
Markets are noisy and largely efficient, and even a small predictive edge can be
useful when combined with appropriate execution and risk management.
""")

st.divider()


# ============================
# BACKTESTING
# ============================
st.subheader("4. Strategy Backtest")

with st.spinner("Running trade-level backtest..."):
    bt_df, total_return, win_rate = backtest(
        df_feat, model, features
    )

col1, col2, col3 = st.columns(3)
col1.metric("Total Return (%)", f"{total_return:.2f}")
col2.metric("Win Rate (%)", f"{win_rate:.2f}")
col3.metric("Trades Executed", "Calculated internally")

st.line_chart(bt_df["close"], height=300)

st.markdown("""
### Interpretation of Results

- **Total Return**  
  Measures the percentage change in account equity over the backtest period,
  assuming one open position at a time and no leverage.

- **Win Rate**  
  Percentage of completed trades that resulted in positive returns.
  This is calculated at the trade level, not per candle.

- **Accuracy**  
  Reflects classification performance on the prediction task, not trading profitability.

### Important Notes
- Transaction costs, slippage, and spreads are not included
- Results are for research and demonstration purposes only
- Live trading performance will differ
""")

st.divider()


# ============================
# SYSTEM SUMMARY
# ============================
st.subheader("System Design Summary")

st.markdown("""
**Model**
- Random Forest classifier
- Volatility-filtered directional target
- Class-balanced training
- Time-aware train/test split

**Signal Generation**
- Probability-based decision thresholds
- Trades taken only under higher-confidence conditions
- Neutral state during low-confidence periods

**Backtesting Engine**
- One position at a time
- Explicit trade entry and exit
- Trade-level profit and loss calculation
- Realistic performance metrics

The system is designed to prioritize methodological correctness and transparency
over exaggerated performance claims.
""")

st.success("System execution completed successfully.")

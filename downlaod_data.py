import yfinance as yf
import pandas as pd
import os

# ===============================
# Create data folder if not exists
# ===============================
os.makedirs("data", exist_ok=True)

# ===============================
# Forex pair (Yahoo Finance symbol)
# ===============================
PAIR = "EURUSD=X"

# ===============================
# Download data (Yahoo limit: 1H max 2y)
# ===============================
forex_ml_dataset = yf.download(
    PAIR,
    interval="1h",
    period="2y",
    auto_adjust=False,
    group_by="column"
)

# ===============================
# Safety check
# ===============================
if forex_ml_dataset.empty:
    raise ValueError("No data downloaded. Check Yahoo Finance limits.")

# ===============================
# Reset index
# ===============================
forex_ml_dataset = forex_ml_dataset.reset_index()

# ===============================
# FIX: Flatten MultiIndex columns
# ===============================
forex_ml_dataset.columns = [
    col[0].lower() if isinstance(col, tuple) else col.lower()
    for col in forex_ml_dataset.columns
]

# ===============================
# Rename time column
# ===============================
if "datetime" in forex_ml_dataset.columns:
    forex_ml_dataset = forex_ml_dataset.rename(columns={"datetime": "time"})
elif "date" in forex_ml_dataset.columns:
    forex_ml_dataset = forex_ml_dataset.rename(columns={"date": "time"})

# ===============================
# Keep only OHLCV
# ===============================
forex_ml_dataset = forex_ml_dataset[["time", "open", "high", "low", "close", "volume"]]

# ===============================
# Save CSV
# ===============================
forex_ml_dataset.to_csv("data/eurusd.csv", index=False)

print("===================================")
print(f"Downloaded {len(forex_ml_dataset)} rows of EURUSD")
print("Saved to data/eurusd.csv")
print("===================================")

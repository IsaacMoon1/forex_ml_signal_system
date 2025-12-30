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
df = yf.download(
    PAIR,
    interval="1h",
    period="2y",
    auto_adjust=False,
    group_by="column"
)

# ===============================
# Safety check
# ===============================
if df.empty:
    raise ValueError("No data downloaded. Check Yahoo Finance limits.")

# ===============================
# Reset index
# ===============================
df = df.reset_index()

# ===============================
# FIX: Flatten MultiIndex columns
# ===============================
df.columns = [
    col[0].lower() if isinstance(col, tuple) else col.lower()
    for col in df.columns
]

# ===============================
# Rename time column
# ===============================
if "datetime" in df.columns:
    df = df.rename(columns={"datetime": "time"})
elif "date" in df.columns:
    df = df.rename(columns={"date": "time"})

# ===============================
# Keep only OHLCV
# ===============================
df = df[["time", "open", "high", "low", "close", "volume"]]

# ===============================
# Save CSV
# ===============================
df.to_csv("data/eurusd.csv", index=False)

print("===================================")
print(f"Downloaded {len(df)} rows of EURUSD")
print("Saved to data/eurusd.csv")
print("===================================")

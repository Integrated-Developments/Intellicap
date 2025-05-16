Version = [0,0,10] 
State = "SCR"

import os
import json
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime

# Set up directories (data folder will be added later)
DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = DIR  # Using DIR for now, will update when data folder is added

def load_market_data():
    """Reads and processes all market JSON data into a DataFrame."""
    data_list = []

    for filename in os.listdir(DATA_DIR):
        if filename.startswith("Market_") and filename.endswith(".json"):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, "r") as f:
                try:
                    json_data = json.load(f)

                    for time_key, values in json_data.items():
                        timestamp = datetime.strptime(f"{filename[7:-5]} {time_key.replace('_', ':')}", "%Y-%m-%d %H:%M")

                        # Extract Open and Close from Average Price
                        open_price = values.get("average_price", None)
                        close_price = values.get("average_price", None)

                        # Extract Low from Lowest Price
                        low_price = values.get("lowest_price", None)

                        # Extract High Price from Raw Data (Find highest listing price)
                        high_price = max([listing["cost"] for listing in values["raw_data"]["pointsmarket"].values()], default=None)

                        # Extract Volume
                        volume = values.get("total_volume", None)

                        # Append processed data
                        data_list.append({
                            "datetime": timestamp,
                            "Open": open_price,
                            "High": high_price,
                            "Low": low_price,
                            "Close": close_price,
                            "Volume": volume
                        })

                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    print(f"[WARNING] Skipping corrupted file: {filename}, Error: {e}")

    # Convert to Pandas DataFrame
    df = pd.DataFrame(data_list)
    df.sort_values("datetime", inplace=True)  # Ensure chronological order
    return df

def calculate_rsi(series, period=14):
    """Calculates the Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_candlestick_chart(interval="5T", sma_period=10, ema_period=20, rsi_period=14):
    """Processes data into OHLC format and plots a candlestick chart with sub-charts."""
    df = load_market_data()

    if df.empty:
        print("[ERROR] No data found to generate chart.")
        return

    # Resampling data to create OHLC candles
    ohlc_df = df.resample(interval, on="datetime").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    ohlc_df.dropna(inplace=True)  # Remove incomplete candles

    # Ensure we have data before computing indicators
    if ohlc_df.empty:
        print("[ERROR] No valid OHLC data after resampling.")
        return

    # Calculate Moving Averages (SMA & EMA)
    if not ohlc_df["Close"].isna().all():
        ohlc_df["SMA"] = ohlc_df["Close"].rolling(window=sma_period).mean()
        ohlc_df["EMA"] = ohlc_df["Close"].ewm(span=ema_period, adjust=False).mean()
    else:
        ohlc_df["SMA"], ohlc_df["EMA"] = None, None  # Prevent plotting errors

    # Calculate RSI
    if not ohlc_df["Close"].isna().all():
        ohlc_df["RSI"] = calculate_rsi(ohlc_df["Close"], period=rsi_period)
    else:
        ohlc_df["RSI"] = None  # Prevent plotting errors

    # Get the latest average price for the label
    latest_price = ohlc_df["Close"].iloc[-1] if not ohlc_df["Close"].isna().all() else "N/A"

    # Create Additional Plots for Volume, RSI, and Moving Averages
    apds = []
    panel_ratios = [3]  # Main chart panel

    # Only add Volume if it's not empty
    if not ohlc_df["Volume"].isna().all():
        apds.append(mpf.make_addplot(ohlc_df["Volume"], panel=len(panel_ratios), color="purple", alpha=0.5, ylabel="Volume"))
        panel_ratios.append(1)

    # Only add RSI if it's not empty
    if not ohlc_df["RSI"].isna().all():
        apds.append(mpf.make_addplot(ohlc_df["RSI"], panel=len(panel_ratios), color="green", ylabel="RSI"))
        panel_ratios.append(1)

    # Only add Moving Averages if they're not empty
    if not ohlc_df["SMA"].isna().all() and not ohlc_df["EMA"].isna().all():
        apds.append(mpf.make_addplot(ohlc_df["SMA"], panel=len(panel_ratios), color="blue", linestyle="-", label=f"SMA {sma_period}"))
        apds.append(mpf.make_addplot(ohlc_df["EMA"], panel=len(panel_ratios), color="red", linestyle="--", label=f"EMA {ema_period}"))
        panel_ratios.append(1)

    # Ensure at least one sub-panel exists
    if not apds:
        print("[ERROR] No valid data to plot.")
        return

    # Define panel layout dynamically
    fig, axes = mpf.plot(
        ohlc_df,
        type="candle",
        style="charles",
        title=f"Torn Market Candlestick Chart ({interval} Interval)",
        ylabel="Price",
        addplot=apds,
        volume=False,
        figratio=(10, 8),
        panel_ratios=panel_ratios,  # Adjust panels dynamically
        returnfig=True  # Get figure object to modify
    )

    # Add Price Label
    axes[0].text(
        0.02, 0.93, f"Current Avg Price: {latest_price:.2f}",
        transform=axes[0].transAxes, fontsize=12,
        bbox=dict(facecolor='yellow', alpha=0.5)
    )

    plt.show()  # Display the plot

if __name__ == "__main__":
    interval = "5T"  # Default interval for Pydroid testing
    print(f"[INFO] Generating Candlestick Chart with Volume & RSI for {interval} interval...")
    generate_candlestick_chart(interval=interval, sma_period=10, ema_period=20, rsi_period=14)
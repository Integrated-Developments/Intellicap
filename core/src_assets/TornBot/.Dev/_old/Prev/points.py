import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Torn API key (Replace with your actual key)
API_KEY = "mdHz0qLMvoYFQhLJ"

# API URL
API_URL = f"https://api.torn.com/market/?selections=pointsmarket&key={API_KEY}"

# Storage for data
data = []

def fetch_points_market():
    """Fetch the Torn Points Market data from the API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise error if request fails
        market_data = response.json()

        if "pointsmarket" in market_data:
            listings = market_data["pointsmarket"]
            lowest_price = min([listing["cost"] for listing in listings.values()])
            timestamp = datetime.now()

            # Store the data
            data.append({"timestamp": timestamp, "lowest_price": lowest_price})

            print(f"[{timestamp}] Lowest Points Price: {lowest_price} T$")

    except Exception as e:
        print(f"Error fetching data: {e}")

def plot_data():
    """Plot the lowest listing price over time."""
    if not data:
        print("No data to plot.")
        return

    df = pd.DataFrame(data)
    
    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["lowest_price"], marker='o', linestyle='-', label="Lowest Points Price")
    plt.xlabel("Time")
    plt.ylabel("Price (T$)")
    plt.title("Torn Points Market - Lowest Listing Price Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

# Main loop
try:
    while True:
        fetch_points_market()
        time.sleep(60)  # Wait for 1 minute before the next request
except KeyboardInterrupt:
    print("\nStopping script and displaying chart.")
    plot_data()
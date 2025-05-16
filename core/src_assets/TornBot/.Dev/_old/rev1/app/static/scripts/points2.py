Version = [0,0,4]
State = "SCR"

import requests
import json
import os
import time
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))
Dat_DIR = os.path.join (DIR, "data")
Sys_DIR = os.path.join (Dat_DIR, "console")

key = None

patx = os.path.join(Dat_DIR, "user.json")
with open (patx, 'r') as f :
    xxf = json.load(f)
    key = xxf['My_Data']['key']

def timer (x=int) :
    for x in range(x) :
        print (f"[INFO] {x}")

API_URL = f"https://api.torn.com/market/?selections=pointsmarket&key={key}"
Curl = f"curl -X 'GET' 'https://api.torn.com/v2/market?selections=pointsmarket' -H 'accept: application/json' -H 'Authorization: ApiKey {key}'"

def fetch_points_market():
    print("\n[DEBUG] Fetching Points Market Data...")
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        market_data = response.json()
        print("[DEBUG] API Call Successful. Processing Data...")
        if "pointsmarket" in market_data:
            listings = market_data["pointsmarket"]
            print(f"[DEBUG] Received {len(listings)} listings.")
            lowest_price = min([listing["cost"] for listing in listings.values()])
            total_volume = sum([listing["quantity"] for listing in listings.values()])
            market_cap = sum([listing["total_cost"] for listing in listings.values()])
            average_price = round(market_cap / total_volume, 2) if total_volume > 0 else 0
            timestamp = datetime.now()
            time_key = timestamp.strftime("%H_%M")
            date_str = timestamp.strftime("%Y-%m-%d")
            print(f"[DEBUG] Extracted Data -> Lowest: {lowest_price}, Volume: {total_volume}, Market Cap: {market_cap}, Avg: {average_price}")
            result = {
                "lowest_price": lowest_price,
                "total_volume": total_volume,
                "market_cap": market_cap,
                "average_price": average_price,
                "raw_data": market_data
            }
            save_to_json(date_str, time_key, result)
            print(f"[{time_key}] Lowest Price: {lowest_price}, Volume: {total_volume}, Market Cap: {market_cap}, Avg Price: {average_price}")
        else:
            print("[ERROR] 'pointsmarket' key missing in API response.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API Request Failed: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")

def save_to_json(date_str, time_key, result):
    filename = f"Market_{date_str}.json"
    print(f"[DEBUG] Saving Data to {filename}...")
    if os.path.exists(filename):
        print(f"[DEBUG] {filename} exists. Loading existing data...")
        with open(filename, "r") as file:
            try:
                data = json.load(file)
                print("[DEBUG] Successfully loaded existing JSON data.")
            except json.JSONDecodeError:
                print("[WARNING] JSON file was corrupted or empty. Creating a new structure.")
                data = {}
    else:
        print(f"[DEBUG] {filename} does not exist. Creating new JSON file.")
        data = {}
    print(f"[DEBUG] Adding new entry for {time_key}...")
    data[time_key] = result
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"[DEBUG] Successfully updated {filename}.")
    
if __name__ == "__main__" :
    print("[DEBUG] Starting Market Tracking Script...")
    fetch_points_market()

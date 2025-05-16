import requests #type:ignore
import json #type:ignore
import datetime #type:ignore
import os, sys #type:ignore
import time #type:ignore

key = 'crn2ajpr01qmi0u6jsigcrn2ajpr01qmi0u6jsj0'
symbol = 'OXSQ'

url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={key}'


def Base_Directory () :
    if getattr(sys, 'frozen', False) :
        _dir = os.path.dirname (sys.executable)
    else:
        _dir = os.path.dirname(os.path.abspath(__file__))
    dat_dir = os.path.join (_dir, "data")

def Prints (*args) :
    for txt in args :
        print (txt)
        print ("")
    time.sleep (1)

# Make the request
response = requests.get(url)

# Parse the response as JSON
data = response.json()
print (data)
# Print the stock data
print(f"Current price for {symbol}: {data['c']}")
print(f"High price of the day: {data['h']}")
print(f"Low price of the day: {data['l']}")
print(f"Opening price: {data['o']}")
print(f"Previous closing price: {data['pc']}")
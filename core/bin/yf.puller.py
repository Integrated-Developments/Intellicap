# <!-- [SS-0]: Meta Data ----->
VERSION = "0.1.0"
DATE = "6.24.25"
DESCRIPTION = "Parallel Async YF Puller"
DEV = "AngrySatan666"

# <!-- [SS-1]: Imports ----->
import yfinance as yf
import pandas as pd
import os
import concurrent.futures
import argparse
import sys

# <!-- [SS-2]: Global Variables ----->
_dir = os.path.dirname(os.path.abspath(__file__))
concatenate = 0
con_err = []

# <!-- [SS-3]: Snippetype Functions ----->
def prints (*args) :
    for txt in args :
        print (txt)
        print (" ")

# <!-- [SS-4]: Script Functions ----->
def Pull(symbols, intervals, start=None, end=None, threads=8, outpath=None):
    """
    Download intraday historical charts for multiple symbols and intervals in parallel.
    Saves results as a pickle file to outpath, or prints summary if outpath is None.
    """

    # <!-- [SS-4.1]: Local Variables --->
    results = {}
    max_workers = min(threads, 5)

    # <!-- [SS-4.2]: Local Functions --->
    def fetch(symbol, interval):
        global concatenate, con_err
        try:
            if start is not None and end is not None:
                df = yf.download(symbol, interval=interval, start=start, end=end, auto_adjust=True)
            elif start is not None and end is None:
                raise TypeError("End date must be provided if start date is specified.")
            elif start is None and end is not None:
                raise TypeError("Start date must be provided if end date is specified.")
            else:
                df = yf.download(symbol, interval=interval, auto_adjust=True)
            return (symbol, interval, df)
        except Exception as e:
            if "No objects to concatenate" in str(e):
                concatenate += 1
                err = (f"Concatenation error for [{symbol}: {interval} chart]: {e}")
                con_err.append(err)
            else:
                prints(f"Warning: Failed to fetch {symbol} [{interval}]: {e}")
        if concatenate != 0:
            return (symbol, interval, None)

    # <!-- [SS-4.3]: Thread Pool Executor --->
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for symbol in symbols:
            for interval in intervals:
                futures.append(executor.submit(fetch, symbol, interval))
        for future in concurrent.futures.as_completed(futures):
            symbol, interval, df = future.result()
            if df is not None:
                if symbol not in results:
                    results[symbol] = {}
                results[symbol][interval] = df

    if outpath is not None:
        pd.to_pickle(results, outpath)
        prints(f"Saved data to {outpath}")
    else:
        for symbol in results:
            for interval in results[symbol]:
                df = results[symbol][interval]
                prints(f"{symbol} [{interval}]: {len(df)} rows")

# <!-- [SS-5]: Runnit ----->
if __name__ == "__main__":
    # <!-- [SS-5.1]: Argument Parsing --->
    parser = argparse.ArgumentParser(description="Parallel Async YF Puller")
    parser.add_argument("--symbols", type=str, default="SPY,AMD,COIN,SMCI,AAPL,GOOGL,MSFT,AMZN,TSLA", help="Comma-separated list of stock symbols (e.g. AAPL,GOOGL,MSFT)")
    parser.add_argument("--intervals", type=str, default="1m,5m,15m", help="Comma-separated list of intervals (e.g. 1m,5m,15m)")
    parser.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD)")
    parser.add_argument("--outpath", type=str, default=f"_dir", help="Output pickle file path")
    args = parser.parse_args()

    # <!-- [SS-5.2]: Check if Terminal --->
    if sys.stdin.isatty():
        prints("Running in interactive/terminal mode.")
        prints("Using defaults")
        Pull (
            symbols=args.symbols.split(","),
            intervals=args.intervals.split(","),
            start=args.start,
            end=args.end,
            outpath=args.outpath
        )
    else:
        prints("Running in non-interactive/subprocess mode.")
        if args.symbols:
            symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
        else:
            symbols = ["SPY", "AMD", "COIN", "SMCI", "", "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
        if args.intervals:
            intervals = [i.strip() for i in args.intervals.split(",") if i.strip()]
        else:
            intervals = ["1m", "5m", "15m"]
        if args.start:
            start = args.start.strip()
        else:
            start = None
        if args.end:
            end = args.end.strip()
        else:
            end = None
        if args.outpath is not None:
            outpath = args.outpath.strip()
        else:
            outpath = None
        Pull(
            symbols,
            intervals,
            start,
            end,
            outpath
        )

import subprocess
import json
import time
import sys
from pathlib import Path
import speedtest # pip install speedtest-cli
import psutil
from ping3 import ping

data_dir = None
logs_dir = None

def base_directory():
    global data_dir, logs_dir
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).resolve().parent

    data_dir = base_dir / "data"
    logs_dir = base_dir / "log"

    # Ensure directories exist
    data_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

def load_run_count(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"runs": 0}

def save_run_count(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def parse_netstat():
    try:
        result = subprocess.run(['netstat', '-e'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        data = {}

        for line in lines:
            if "Bytes" in line:
                parts = line.split()
                if len(parts) >= 4:
                    data["Bytes"] = {"Received": parts[2], "Sent": parts[3]}
            elif "Unicast packets" in line:
                parts = line.split()
                if len(parts) >= 4:
                    data['Unicast_Packets'] = {"Received": parts[2], "Sent": parts[3]}
            elif "Non-unicast packets" in line:
                parts = line.split()
                if len(parts) >= 4:
                    data['Non_Unicast_Packets'] = {"Received": parts[2], "Sent": parts[3]}
            elif "Discards" in line:
                parts = line.split()
                if len(parts) >= 4:
                    data['Discards'] = {"Received": parts[2], "Sent": parts[3]}
            elif "Errors" in line:
                parts = line.split()
                if len(parts) >= 4:
                    data['Errors'] = {"Received": parts[2], "Sent": parts[3]}
            elif "Unknown protocols" in line:
                parts = line.split()
                if len(parts) >= 3:
                    data['Unknown_Protocols'] = parts[2]
        
        return data
    except subprocess.CalledProcessError as e:
        print(f"Error running netstat: {e}")
        return {}

def run_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping
        return {
            "Download Speed": f"{download_speed:.2f} Mbps",
            "Upload Speed": f"{upload_speed:.2f} Mbps",
            "Ping": f"{ping} ms"
        }
    except Exception as e:
        print(f"Error running speedtest: {e}")
        return {}

def monitor_bandwidth(interval=1):
    initial = psutil.net_io_counters()
    time.sleep(interval)
    final = psutil.net_io_counters()
    
    bytes_sent = final.bytes_sent - initial.bytes_sent
    bytes_recv = final.bytes_recv - initial.bytes_recv

    return {
        "Bytes Sent": f"{bytes_sent / 1024:.2f} KB",
        "Bytes Received": f"{bytes_recv / 1024:.2f} KB"
    }

def test_ping(target):
    delay = ping(target)
    if delay is not None:
        return f"Ping to {target}: {delay * 1000:.2f} ms"
    else:
        return f"Ping to {target} failed."

def log_results(log_path, results):
    with open(log_path, 'w') as file:
        json.dump(results, file, indent=4)

def test_network():
    results = {}

    print("Running NetStat")
    results["Net Stat"] = parse_netstat()

    print("Starting Speed Test")
    results["Speed Test"] = run_speedtest()

    print("Monitoring Bandwidth")
    results["Bandwidth Usage"] = monitor_bandwidth()

    print("Pinging Google")
    results["Ping Test"] = test_ping("8.8.8.8")

    print("Compiling Data")
    return results

def main():
    global data_dir, logs_dir

    sys_file = data_dir / 'sys.json'
    sys_data = load_run_count(sys_file)
    sys_data['runs'] += 1
    
    print("Press Enter to Start the Test")
    input()

    results = test_network()
    
    log_file = logs_dir / f'net_test_{sys_data["runs"]}.json'
    log_results(log_file, results)

    save_run_count(sys_file, sys_data)
    print("Results Saved", results)

if __name__ == "__main__":
    base_directory()
    main()

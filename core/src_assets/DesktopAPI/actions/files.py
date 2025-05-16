import os
import sys
import json
import argparse
from datetime import datetime

def list_directory(directory):
    result = {}
    for root, dirs, files in os.walk(directory):
        relative_root = "\\" + os.path.relpath(root, directory).replace("\\", "\\\\")
        result[relative_root] = {}
        for file in files:
            result[relative_root][f"\\{file}"] = "FILE"
    return result  

def log_event(log_dir, api_key, directory, response):
    log_path = os.path.join(log_dir, "action_log", "files", "list.json")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)   

    log_data = {
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"): {
            "Status": [api_key, directory],
            "Response": response
        }
    }
    try:
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as file:
                existing_logs = json.load(file)
        else:
            existing_logs = {}

        existing_logs.update(log_data)

        with open(log_path, "w", encoding="utf-8") as file:
            json.dump(existing_logs, file, indent=4, sort_keys=True)
    except Exception as e:
        print(f"Error logging event: {e}", file=sys.stderr)

def main():
    global log_dir
    if getattr(sys, 'frozen', False) :
        _dir = os.path.dirname(sys.executable)
    else:
        _dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join (_dir, "logs", "action_log", "files", "list_log", "list.json")

    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=str, required=True, help="JSON payload")
    parser.add_argument("--log_dir", type=str, required=True, help="Log directory path")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload)

        action = payload.get("action")
        api_key = payload.get("api_key")
        function = payload["args"].get("function")
        directory = payload["args"].get("arg")

        if action != "files" or function != "list":
            print("Unsupported action or function", file=sys.stderr)
            sys.exit(1)

        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
            sys.exit(1)

        response = list_directory(directory)
        print(json.dumps(response, indent=4))
        log_event(args.log_dir, api_key, directory, response)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

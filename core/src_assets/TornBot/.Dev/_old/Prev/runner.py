Version = [0,0,1]
State = "SCR"

import subprocess
import time
from datetime import datetime

# Path to points2.py
POINTS_SCRIPT = "points2.py"

def run_script():
    """Runs points2.py as a separate process."""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Running {POINTS_SCRIPT}...")
        subprocess.run(["python", POINTS_SCRIPT], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to execute {POINTS_SCRIPT}: {e}")

def run_scheduler():
    """Runs points2.py once per minute."""
    last_run_minute = None

    while True:
        now = datetime.now()
        current_minute = now.minute

        if current_minute != last_run_minute:  # Ensure only one execution per minute
            run_script()
            last_run_minute = current_minute

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    print("[INFO] Starting script scheduler...")
    run_scheduler()

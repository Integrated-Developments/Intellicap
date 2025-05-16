Version = [0,1,0]
State = "FSK"

# ----- Imports ----- #
from app import app
import subprocess
import time
from datetime import datetime
import os

# ----- Variables ----- #
POINTS_SCRIPT = os.path.join("app", "static", "scripts", "points2.py")

# ----- Simple Functions ----- #
def prints (x) :
    print (x)
    print ("")

# ----- Script Functions ----- #
def run_script():       """Runs points2.py as a separate process."""
    try:
        prints(f"[{datetime.now().strftime('%H:%M:%S')}] Running {POINTS_SCRIPT}...")
        subprocess.run(["python", POINTS_SCRIPT], check=True)
    except subprocess.CalledProcessError as e:
        prints(f"[ERROR] Failed to execute {POINTS_SCRIPT}: {e}")

# ----- Master Functions ----- #
def run_scheduler():        """Runs points2.py once per minute."""
    last_run_minute = None
    
    while True:
        now = datetime.now()
        current_minute = now.minute

        if current_minute != last_run_minute:  # Ensure only one execution per minute
            run_script()
            last_run_minute = current_minute

        time.sleep(1)  # Check every second

# ----- RUN ----- #
if __name__ == "__main__":
    prints("[INFO] Starting script scheduler...")
    run_scheduler()

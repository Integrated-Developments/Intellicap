import subprocess
import time

def start_ngrok():
    """Start ngrok and wait for the connection."""
    try:
        # Start ngrok
        ngrok_process = subprocess.Popen(
            ["ngrok", "start", "flask"],  # Replace "flask" with your tunnel name
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensures output is in string format
        )
        print("Starting ngrok...")
        # Wait 3 seconds to give ngrok time to connect
        time.sleep(3)
        print("Ngrok should be ready.")
        return ngrok_process
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None

def start_flask():
    try:
        print("Starting Flask app...")
        subprocess.run(["python", "desk_flask.py"])
    except Exception as e:
        print(f"Error starting Flask app: {e}")

if __name__ == "__main__":
    ngrok = start_ngrok()
    if ngrok:
        start_flask()

import os
import ctypes
import subprocess
import time

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except :
        subprocess.run([
            'powershell',
            '-Command',
            f'Start-Process', 'python server.py -Verb RunAs'
        ])

# Start Flask app (adjust path as needed)
flask_proc = subprocess.Popen([
    'cmd.exe', '/k', 'python C:/.Repo/Intellicap/core/run.py'
])

# Wait a few seconds for Flask to start
time.sleep(3)

# Start cloudflared tunnel
cloudflared_proc = subprocess.Popen([
    'cmd.exe', '/k', 'cloudflared tunnel run flask'
])

# Optional: Keep window open (wait for both processes to finish)
flask_proc.wait()
cloudflared_proc.wait()

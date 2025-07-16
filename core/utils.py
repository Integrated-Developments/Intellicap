import os
import shutil
import subprocess
import random, string
import yaml
import socket
import time

_dir = os.path.dirname(os.path.abspath(__file__))
usr_def = os.path.join(_dir, 'dev', 'default')
cfd = os.path.expanduser('~/.cloudflared')

def GenString(char=None, mult=None):
    """Generate a list of multiple random strings of specified length."""
    """Usage. str = GenString(char=3 mult=4) would give ['aks', 'ojd', 'mjo', 'jsp']"""
    """Usage. to see just one in the list str[2] would gie 'mjo' """
    strings = []
    if not isinstance(mult, int):
        mult = 1
    if not isinstance(char, int):
        char = random.choice(range(8, 16))
    for _ in range(mult):
        result = ''.join(random.choices(string.ascii_letters + string.digits, k=char))
        strings.append(result)
        return strings

class Coder :
    """Session Manager for Code Sessions"""
    def __init__(self):
        self.root = os.path.join(_dir, 'dev')

    def Start_Session(self, user, timeout=30):
        """Start the code session for a user, launching code-server on a random port."""
        """Wait for confirmation of both tunnel and code-server."""
        file = f"/home/{user}/{user}.code-workspace"
        try:
            tunnel = f"code.{user}.{GenString(char=3)[0]}"
            before = set(os.listdir(cfd))
            result = subprocess.run(['cloudflared', 'tunnel', 'create', tunnel], capture_output=True, text=True)
            if result.returncode == 0:
                after = set(os.listdir(cfd))
                new = after - before
                creds = os.path.join(cfd, new.pop())
                while True:
                    port = random.choice(range(1000, 10000))
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        try:
                            s.bind(('127.0.0.1', port))
                            break
                        except OSError:
                            continue
                sub = f"code-{user}-{GenString(char=3)[0]}"
                host = f"{sub}.intellicap.org"
                config = {
                    "tunnel": tunnel,
                    "credentials-file": creds,
                    "ingress": [
                        {
                            "hostname": host,
                            "service": f"http://localhost:{port}"
                        },
                        {
                            "service": "http_status:404"
                        }
                    ]
                }
                with open(os.path.join(cfd, f"{tunnel}.yaml"), 'w') as f:
                    yaml.dump(config, f, default_flow_style=False)
                dnns = subprocess.run(['cloudflared', 'tunnel', 'route', 'dns', tunnel, host], capture_output=True, text=True)
                if dnns.returncode == 0:
                    test_bat = os.path.abspath(os.path.join(_dir, 'bin', 'code.bat'))
                    # Call code.bat with port and user as arguments
                    serv_code = [
                        test_bat,
                        str(port),
                        user
                    ]
                    subprocess.Popen(serv_code)
                    tunnel_proc = subprocess.Popen([
                        'cloudflared', 'tunnel', '--config', os.path.join(cfd, f"{tunnel}.yaml"), 'run', tunnel
                    ])
                    code_server_ready = False
                    while True:
                        try:
                            with socket.create_connection(('127.0.0.1', port), timeout=1):
                                code_server_ready = True
                                break
                        except Exception:
                            time.sleep(3)
                    if not code_server_ready:
                        tunnel_proc.terminate()
                        return f"error: code-server did not start on port {port}"
                    if tunnel_proc.poll() is not None:
                        return f"error: tunnel process failed to start"
                    return f"https://{host}"
                else:
                    return "error: tunnel DNS setup failed"
            else:
                return "error: tunnel creation failed"
        except Exception as e:
            return f"error: {str(e)}"


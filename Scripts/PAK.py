import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

_dir = "C:\\Intellicap"
reqs_file = os.path.join("Scripts", "reqs.txt")

def get_reqs(file):
    with open(file, "r") as f:
        return [
            line.strip() for line in f.readlines()
            if line.strip() and not line.strip().startswith("#")
        ]

def get_installed_packages():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=freeze"],
        capture_output=True, text=True
    )
    pkgs = []
    for line in result.stdout.splitlines():
        if "==" in line:
            pkgs.append(line.split("==")[0])
    return pkgs

def pip_cmd(args):
    return subprocess.run([sys.executable, "-m", "pip"] + args,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process_packages(packages, upgrade=False):
    cmd = ["install"]
    if upgrade:
        cmd.append("--upgrade")
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(pip_cmd, cmd + [pkg]): pkg for pkg in packages
        }
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Processing", unit="pkg"):
            pass

def main():
    if "--update" in sys.argv:
        pkgs = get_installed_packages()
        process_packages(pkgs, upgrade=True)
    else:
        pkgs = get_reqs(reqs_file)
        process_packages(pkgs)

if __name__ == "__main__":
    main()

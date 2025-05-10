import sys
import subprocess
import configparser
import os

DEFAULT_BRANCH = "main"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'gittr.cfg')

def ensure_config_exists():
    """Create config file if it doesn't exist"""
    if not os.path.exists(CONFIG_FILE):
        config = configparser.ConfigParser()
        config['gittr'] = {}
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)

def is_git_repo():
    """Check if the current directory is inside a git repository."""
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def run_git_command(*args):
    """Helper function to run Git commands safely."""
    try:
        subprocess.run(["git"] + list(args), check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        sys.exit(1)

def update_counter(command):
    """Updates the counter for the specified command in gittr.cfg"""
    ensure_config_exists()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    current = config['gittr'].get(command, '0')
    next_val = str(int(current) + 1)
    config['gittr'][command] = next_val
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    return next_val

def get_commit_message(command='commit'):
    """Gets commit message with counter for specific command"""
    count = update_counter(command)
    return f"gittr --{command} #{count}"

def commit_changes(command='commit'):
    """Stages, adds all files, and commits with command-specific message."""
    run_git_command("add", ".")
    commit_msg = get_commit_message(command)
    run_git_command("commit", "-m", commit_msg)
    print(f"✅ Committed: {commit_msg}")

def push_changes(branch):
    """Pushes the latest committed changes."""
    run_git_command("push", "origin", branch)
    print(f"🚀 Pushed to {branch}")

def shove_changes():
    """Combines commit and push into a single operation."""
    commit_changes('shove')
    push_changes(DEFAULT_BRANCH)

def create_issue():
    """Opens a new GitHub issue (requires remote repo)."""
    title = input("Enter issue title: ")
    body = input("Enter issue description: ")
    run_git_command("issue", "create", "--title", title, "--body", body)
    print(f"🔖 Issue '{title}' created.")

def pull_changes():
    """Pulls the latest changes from the default branch."""
    run_git_command("pull", "origin", DEFAULT_BRANCH)
    print(f"🔄 Pulled latest changes from {DEFAULT_BRANCH}")

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--commit" in args:
        commit_changes()
    if "--push" in args:
        push_changes(DEFAULT_BRANCH)
    if "--shove" in args:
        shove_changes()
    if "--issue" in args:
        create_issue()
    if "--pull" in args:
        pull_changes()
    
    if not args:
        print("Usage: gittr.py --commit | --push | --shove | --issue | --pull")
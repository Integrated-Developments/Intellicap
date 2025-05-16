import subprocess

def open_application(application_path: str) -> str:
    """Open an application given its file path."""
    try:
        subprocess.Popen(application_path, shell=True)
        return f"Application {application_path} opened successfully."
    except Exception as e:
        return f"Failed to open application: {e}"

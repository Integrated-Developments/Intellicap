## ----- Imports ------ ##
import sys
import json
from PIL import ImageGrab

## ----- MAIN ----- ##
def main():
    # Validate and parse input
    if len(sys.argv) < 2:
        print("Error: JSON data required as argument.")
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Invalid JSON input.")
        sys.exit(1)

    # Validate path in JSON
    if "path" not in data:
        print("Error: Missing 'path' key in JSON data.")
        sys.exit(1)

    file_path = data["path"]

    # Take a screenshot
    screenshot = ImageGrab.grab()
    screenshot.save(file_path, "PNG")
    print(f"Screenshot saved to {file_path}")


if __name__ == "__main__":
    main()
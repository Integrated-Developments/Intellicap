## ----- Imports ------ ##
from flask import Flask, request, jsonify, send_file
import subprocess
import os
import json

## ----- Global Variables ----- ##
app = Flask(__name__)
screenshot_script = "screenshot.py"  # Path to the screenshot script
output_dir = "screenshots"  # Directory to save screenshots

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

## ----- Routes ----- ##
@app.route("/screenshot", methods=["POST"])
def screenshot():
    # Parse JSON request
    try:
        data = request.get_json()
        if not data or "key" not in data or "args" not in data:
            return jsonify({"error": "Invalid JSON data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Generate a unique file name for the screenshot
    file_name = f"{data['key']}_screenshot.png"
    file_path = os.path.join(output_dir, file_name)

    # Run the screenshot script via subprocess
    try:
        subprocess.run(
            ["python", screenshot_script, json.dumps({"path": file_path})],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to run screenshot script: {str(e)}"}), 500

    # Return the screenshot to the requester
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/png")
    else:
        return jsonify({"error": "Screenshot not found"}), 500


## ----- MAIN ----- ##
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
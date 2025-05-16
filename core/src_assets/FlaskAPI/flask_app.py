from flask import Flask, request, jsonify
import requests
import random, string
import json
import datetime
import os

app = Flask(__name__)

## --- Directory --- ##
_dir = ("/home/API666/mysite/")
dat_dir = (f"{_dir}data/")
sta_dir = (f"{_dir}static/")
log_dir = (f"{_dir}logs/")
chats_log = os.path.join(log_dir, 'prores.json')

## --- Load Data --- ##
@app.route('/append_json', methods=['POST'])
def append_json():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400
        if os.path.exists(chats_log):
            with open(chats_log, 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response_pair_id = f"{timestamp}({len(existing_data) + 1})"
        existing_data[response_pair_id] = data
        with open(chats_log, 'w') as file:
            json.dump(existing_data, file, indent=4)
        return jsonify({"status": "success", "message": "Data appended successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_data', methods=['POST'])
def get_data():
    data = requests.json
    file_path = data.get("file_path")
    if not file_path:
        return jsonify({"error": "No file path provided."}), 400
    else :
        files = os.path.join(_dir, file_path)
    if os.path.exists(files):
        with open(files, 'r') as file:
            file_content = file.read()
        return jsonify({"content": file_content, "status": "success"})
    else:
        return jsonify({"error": "File not found.", "status": "failed"}), 404

@app.route('/save_code', methods=['POST'])
def save_code():
    data = requests.get_json()
    if not data or 'code' not in data or 'ext' not in data or 'format' not in data:
        return jsonify({"error": "Missing required fields: 'code', 'ext', or 'format'"}), 400
    code_content = data['code']
    file_ext = data['ext']
    is_formatted = data['format']
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    code_filename = f"parsed_code_{timestamp}{file_ext}"
    if is_formatted:
        code_dir = f'{_dir}data/parsings/formatted'
    else:
        code_dir = f'{_dir}data/parsings/response'
    os.makedirs(code_dir, exist_ok=True)
    code_path = os.path.join(code_dir, code_filename)
    open(code_path, 'w').close()
    with open(code_path, 'w') as file:
        file.write(code_content)
    json_dir = f'{_dir}data/parsings/parsed'
    os.makedirs(json_dir, exist_ok=True)
    json_filename = f"parsed_payload_{timestamp}.json"
    json_path = os.path.join(json_dir, json_filename)
    open(json_path, 'w').close()
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return jsonify({
        "message": "Code and payload saved successfully",
        "code_filename": code_path,
        "json_filename": json_path
    }), 200

@app.route('/admin', methods=(['POST'],['GET']))
def verify () :
    pass

if __name__ == '__main__':
    app.run(debug=True)

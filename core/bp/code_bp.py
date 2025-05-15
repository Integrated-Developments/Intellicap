import os
from flask import Blueprint, request, session, jsonify, send_from_directory
from flask_socketio import emit, join_room, leave_room
from core import socketio
import json
import subprocess

# <!-- Variables ----->
code_bp = Blueprint('code', __name__)
USER_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'user_data')
os.makedirs(USER_DATA_DIR, exist_ok=True)
rooms = {}  # {room_name: {"host": user, "members": set(), "files": {filename: content}}}
PORT_BASE = 9000
MAX_ROOMS = 100
room_ports = {}  # {room_name: port}

# <!-- Functions ----->
def get_available_port():
    used_ports = set(room_ports.values())
    for port in range(PORT_BASE, PORT_BASE + MAX_ROOMS):
        if port not in used_ports:
            return port
    raise RuntimeError("No available ports for code-server.")

def get_room_dir(room_name):
    path = os.path.join(USER_DATA_DIR, room_name)
    os.makedirs(path, exist_ok=True)
    return path

def save_file_to_disk(room_name, filename, content):
    room_dir = get_room_dir(room_name)
    file_path = os.path.join(room_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_file_from_disk(room_name, filename):
    room_dir = get_room_dir(room_name)
    file_path = os.path.join(room_dir, filename)
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def start_code_server(room_name, port):
    room_dir = get_room_dir(room_name)
    cmd = [
        "code-server",
        "--auth", "none",
        "--port", str(port),
        room_dir
    ]
    subprocess.Popen(cmd)

# <!-- Route Logic ----->
@code_bp.route('/room/create', methods=['POST'])
def create_room():
    data = request.json
    room_name = data.get('room_name')
    user = data.get('user')
    workspace_json = data.get('workspace_json')
    devcontainer_json = data.get('devcontainer_json')
    if not room_name or not user:
        return jsonify({"error": "Missing room_name or user"}), 400
    if room_name in rooms:
        return jsonify({"error": "Room already exists"}), 400
    files = {}
    if workspace_json:
        try:
            parsed = json.loads(workspace_json)
            content = json.dumps(parsed, indent=4)
            files['.code-workspace'] = content
        except Exception:
            return jsonify({"error": "Invalid .code-workspace JSON"}), 400
    if devcontainer_json:
        try:
            parsed = json.loads(devcontainer_json)
            content = json.dumps(parsed, indent=4)
            files['devcontainer.json'] = content
        except Exception:
            return jsonify({"error": "Invalid devcontainer.json JSON"}), 400
    rooms[room_name] = {"host": user, "members": set([user]), "files": files}
    for fname, content in files.items():
        save_file_to_disk(room_name, fname, content)
    return jsonify({"success": True, "room": room_name})

@code_bp.route('/room/join', methods=['POST'])
def join_room_http():
    data = request.json
    room_name = data.get('room_name')
    user = data.get('user')
    if not room_name or not user:
        return jsonify({"error": "Missing room_name or user"}), 400
    if room_name not in rooms:
        return jsonify({"error": "Room does not exist"}), 404
    rooms[room_name]["members"].add(user)
    return jsonify({"success": True, "room": room_name})

@code_bp.route('/room/<room_name>/files', methods=['GET'])
def list_files(room_name):
    room_dir = get_room_dir(room_name)
    if not os.path.exists(room_dir):
        return jsonify([])
    return jsonify([f for f in os.listdir(room_dir) if os.path.isfile(os.path.join(room_dir, f))])

@code_bp.route('/room/<room_name>/file/<filename>', methods=['GET'])
def download_file(room_name, filename):
    room_dir = get_room_dir(room_name)
    return send_from_directory(room_dir, filename, as_attachment=True)

@code_bp.route('/room/<room_name>/start_code_server', methods=['POST'])
def start_room_code_server(room_name):
    if room_name in room_ports:
        port = room_ports[room_name]
    else:
        port = get_available_port()
        room_ports[room_name] = port
    start_code_server(room_name, port)
    return jsonify({"success": True, "url": f"http://your-server:{port}/"})

# <!--  SocketIO Events ----->
@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    user = data['user']
    join_room(room)
    if room in rooms:
        rooms[room]["members"].add(user)
        emit('user_joined', {"user": user, "members": list(rooms[room]["members"])}, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    user = data['user']
    leave_room(room)
    if room in rooms and user in rooms[room]["members"]:
        rooms[room]["members"].remove(user)
        emit('user_left', {"user": user, "members": list(rooms[room]["members"])}, room=room)

@socketio.on('open_file')
def handle_open_file(data):
    room = data['room']
    filename = data['filename']
    content = load_file_from_disk(room, filename)
    emit('file_content', {"filename": filename, "content": content})

@socketio.on('save_file')
def handle_save_file(data):
    room = data['room']
    filename = data['filename']
    content = data['content']
    user = data['user']
    save_file_to_disk(room, filename, content)
    emit('file_updated', {"filename": filename, "content": content, "user": user}, room=room, include_self=False)

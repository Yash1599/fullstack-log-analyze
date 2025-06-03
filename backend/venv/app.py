from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import jwt
import datetime
from functools import wraps
import re
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Allow CORS requests from frontend

# Secret key used for signing JWTs
SECRET_KEY = 'super-secret-key'

# Dummy user data
USERS = {
    "admin": "password123"
}

# Create uploads folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------
# JWT Decorator
# ---------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403
        return f(*args, **kwargs)
    return decorated

# ---------------------
# Routes
# ---------------------
@app.route('/')
def index():
    return "✅ Flask Backend is running!"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Basic credential check
    if username in USERS and USERS[username] == password:
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Example protected route (next step)
# @app.route('/upload', methods=['POST'])
# # @token_required
# def upload():
#     return jsonify({"message": "File upload placeholder!"})
@app.route('/upload', methods=['POST'])
@token_required
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Filename is empty"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    ip_count = defaultdict(int)
    parsed_logs = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        match = log_pattern.match(line)

        if not match:
            continue

        log = match.groupdict()
        log["id"] = i
        log["anomaly"] = False
        log["reason"] = ""
        log["confidence"] = 0.0

        ip = log["ip"]
        status = int(log["status"])
        path = log["path"]

        ip_count[ip] += 1

        # Rule 1: Too many requests from same IP
        if ip_count[ip] > 3:
            log["anomaly"] = True
            log["reason"] = f"High frequency from IP {ip}"
            log["confidence"] = 0.8

        # Rule 2: Suspicious path
        if "/admin" in path or "/wp-login" in path:
            log["anomaly"] = True
            log["reason"] = f"Suspicious path: {path}"
            log["confidence"] = max(log["confidence"], 0.9)

        # Rule 3: Error codes
        if status >= 400:
            log["anomaly"] = True
            log["reason"] = f"Returned status code {status}"
            log["confidence"] = max(log["confidence"], 0.7)

        parsed_logs.append(log)

    return jsonify({"logs": parsed_logs})

# Simple log format: IP - - [timestamp] "METHOD PATH PROTOCOL" STATUS
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>.*?) HTTP/1.1" (?P<status>\d+)'
)

# ---------------------
# Run App
# ---------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)

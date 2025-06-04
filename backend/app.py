# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from auth import signup, login
# from anomaly import parse_log_file
# import os
# import jwt
# from functools import wraps


# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend requests

# # Secret key for JWT
# SECRET_KEY = "super-secret"

# # Upload folder
# UPLOAD_FOLDER = './uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # -----------------------------
# # JWT Token Authentication
# # -----------------------------
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'Authorization' in request.headers:
#             parts = request.headers['Authorization'].split()
#             if len(parts) == 2 and parts[0] == "Bearer":
#                 token = parts[1]
#         if not token:
#             return jsonify({'error': 'Token is missing!'}), 403
#         try:
#             jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return jsonify({'error': 'Token has expired!'}), 403
#         except jwt.InvalidTokenError:
#             return jsonify({'error': 'Invalid token!'}), 403
#         return f(*args, **kwargs)
#     return decorated

# # -----------------------------
# # Routes
# # -----------------------------

# @app.route('/')
# def index():
#     return "✅ Flask backend is up and running!"

# # POST /signup – Register a new user
# @app.route('/signup', methods=['POST'])
# def signup_route():
#     return signup()

# # POST /login – Get a JWT token
# @app.route('/login', methods=['POST'])
# def login_route():
#     return login()

# # POST /upload – Upload log file and analyze
# # @app.route('/upload', methods=['POST'])
# # @token_required
# # def upload():
# #     if 'file' not in request.files:
# #         return jsonify({"error": "No file uploaded"}), 400

# #     file = request.files['file']
# #     if file.filename == '':
# #         return jsonify({"error": "Filename is empty"}), 400

# #     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
# #     file.save(file_path)

# #     parsed_logs = parse_log_file(file_path)  # Run AI model

# #     return jsonify({"logs": parsed_logs})


# from flask import request, jsonify
# from anomaly import detect_anomalies
# from auth import token_required

# @app.route("/upload", methods=["POST"])
# @token_required
# def upload():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["file"]
#     lines = file.read().decode("utf-8").splitlines()

#     parsed_logs = detect_anomalies(lines)

#     return jsonify({"logs": parsed_logs})


# # @app.route('/upload', methods=['POST'])
# # @token_required
# # def upload():
# #     if 'file' not in request.files:
# #         return jsonify({"error": "No file uploaded"}), 400

# #     file = request.files['file']
# #     if file.filename == '':
# #         return jsonify({"error": "Filename is empty"}), 400

# #     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
# #     file.save(file_path)

# #     parsed_logs = parse_log_file(file_path)

# #     return jsonify({"logs": parsed_logs})
# # -----------------------------
# # Start Server
# # -----------------------------
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=10000)


from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import signup, login, token_required  # 🔐 Auth functions + JWT decorator
from anomaly import parse_log_file  # 🧠 Anomaly detection
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests (for frontend integration)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------- Auth Routes ---------------------- #

@app.route("/signup", methods=["POST"])
def handle_signup():
    return signup()

@app.route("/login", methods=["POST"])
def handle_login():
    return login()

# ---------------------- Upload & Anomaly Detection ---------------------- #

@app.route("/upload", methods=["POST"])
@token_required
def upload():
    """
    Accepts log file, saves to disk, runs anomaly detection, and returns results.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # ✅ Call the anomaly detection logic
    parsed_logs = parse_log_file(filepath)

    return jsonify({"logs": parsed_logs}), 200

# ---------------------- Run Server ---------------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

from anomaly import parse_log_file
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import jwt
import datetime
from functools import wraps
from anomaly import parse_log_file  # ⬅️ Import from anomaly.py

app = Flask(__name__)

# Configure CORS for production and development
if os.getenv('FLASK_ENV') == 'production':
    # In production, allow your Vercel domain
    CORS(app, origins=["https://*.vercel.app", "https://your-domain.com"])
else:
    # In development, allow localhost
    CORS(app, origins=["http://localhost:3000"])

# Secret key for JWT - use environment variable in production
SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')

# Dummy user database
USERS = {
    "admin": "password123"
}

# Ensure upload directory exists
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
    return "✅ Flask backend is up and running!"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in USERS and USERS[username] == password:
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

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

    parsed_logs = parse_log_file(file_path)  # 👈 Delegate to anomaly.py

    return jsonify({"logs": parsed_logs})

# ---------------------
# Run App
# ---------------------
if __name__ == '__main__':
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

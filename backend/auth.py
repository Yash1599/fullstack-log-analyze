from flask import request, jsonify
from db import users_collection
import jwt, datetime

SECRET_KEY = "super-secret"


def signup():
    data = request.get_json()
    print("Signup received:", data)  # 👈 Add this line

    if users_collection.find_one({"username": data["username"]}):
        return jsonify({"error": "User already exists"}), 400

    users_collection.insert_one({
        "username": data["username"],
        "password": data["password"]
    })
    
    print("User saved to MongoDB")  # 👈 Add this too

    return jsonify({"message": "Signup successful"}), 201

# def signup():
#     data = request.get_json()
#     if users_collection.find_one({"username": data["username"]}):
#         return jsonify({"error": "User already exists"}), 409
#     users_collection.insert_one({
#         "username": data["username"],
#         "password": data["password"]
#     })
#     return jsonify({"message": "Signup successful"})


from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = 'super-secret'  # make sure this is same as the one used in token creation

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

def login():
    data = request.get_json()
    user = users_collection.find_one({
        "username": data["username"],
        "password": data["password"]
    })
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    # token = jwt.encode({
    #     "user": user["username"],
    #     "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    # }, SECRET_KEY, algorithm="HS256")"
    token = jwt.encode(
    {"username": user["username"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
    SECRET_KEY,
    algorithm="HS256"
    )
    return jsonify({"token": token})


# def login():
#     data = request.get_json()
#     user = users_collection.find_one({"username": data["username"]})
#     if not user or not check_password_hash(user["password"], data["password"]):
#         return jsonify({"error": "Invalid credentials"}), 401

#     token = jwt.encode({
#         "username": user["username"],
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
#     }, SECRET_KEY, algorithm="HS256")

#     return jsonify({"token": token})

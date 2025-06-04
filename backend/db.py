from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI") or "mongodb+srv://admin:admin123@cluster0.cylaqrx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["Cluster0"]
users_collection = db["users"]

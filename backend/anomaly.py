# # # import re
# # # from collections import defaultdict

# # # # Regex pattern to match each log entry
# # # log_pattern = re.compile(
# # #     r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>.*?) HTTP/1.1" (?P<status>\d+)'
# # # )

# # # def parse_logs(file_path):
# # #     ip_count = defaultdict(int)
# # #     parsed_logs = []

# # #     with open(file_path, 'r') as f:
# # #         lines = f.readlines()

# # #     for i, line in enumerate(lines):
# # #         line = line.strip()
# # #         match = log_pattern.match(line)

# # #         if not match:
# # #             continue

# # #         log = match.groupdict()
# # #         log["id"] = i
# # #         log["anomaly"] = False
# # #         log["reason"] = ""
# # #         log["confidence"] = 0.0

# # #         ip = log["ip"]
# # #         status = int(log["status"])
# # #         path = log["path"]

# # #         ip_count[ip] += 1

# # #         # Rule 1: Too many requests from same IP
# # #         if ip_count[ip] > 3:
# # #             log["anomaly"] = True
# # #             log["reason"] = f"High frequency from IP {ip}"
# # #             log["confidence"] = 0.8

# # #         # Rule 2: Suspicious path
# # #         if "/admin" in path or "/wp-login" in path:
# # #             log["anomaly"] = True
# # #             log["reason"] = f"Suspicious path: {path}"
# # #             log["confidence"] = max(log["confidence"], 0.9)

# # #         # Rule 3: Error codes
# # #         if status >= 400:
# # #             log["anomaly"] = True
# # #             log["reason"] = f"Returned status code {status}"
# # #             log["confidence"] = max(log["confidence"], 0.7)

# # #         parsed_logs.append(log)

# # #     return parsed_logs
# # import re
# # from collections import defaultdict

# # log_pattern = re.compile(
# #     r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>.*?) HTTP/1.1" (?P<status>\d+)'
# # )

# # def parse_log_file(file_path):
# #     ip_count = defaultdict(int)
# #     parsed_logs = []

# #     with open(file_path, 'r') as f:
# #         lines = f.readlines()

# #     for i, line in enumerate(lines):
# #         line = line.strip()
# #         match = log_pattern.match(line)

# #         if not match:
# #             continue

# #         log = match.groupdict()
# #         log["id"] = i
# #         log["anomaly"] = False
# #         log["reason"] = ""
# #         log["confidence"] = 0.0

# #         ip = log["ip"]
# #         status = int(log["status"])
# #         path = log["path"]

# #         ip_count[ip] += 1

# #         # Rule 1: Too many requests from same IP
# #         if ip_count[ip] > 3:
# #             log["anomaly"] = True
# #             log["reason"] = f"High frequency from IP {ip}"
# #             log["confidence"] = 0.8

# #         # Rule 2: Suspicious path
# #         if "/admin" in path or "/wp-login" in path:
# #             log["anomaly"] = True
# #             log["reason"] = f"Suspicious path: {path}"
# #             log["confidence"] = max(log["confidence"], 0.9)

# #         # Rule 3: Error codes
# #         if status >= 400:
# #             log["anomaly"] = True
# #             log["reason"] = f"Returned status code {status}"
# #             log["confidence"] = max(log["confidence"], 0.7)

# #         parsed_logs.append(log)

# #     return parsed_logs




# # from sentence_transformers import SentenceTransformer
# # from sklearn.ensemble import IsolationForest

# # model = None
# # embedder = None

# # sample_logs = [
# #     "User logged in from 192.168.0.1",
# #     "Session opened for user root",
# #     "Ping google.com",
# #     "Disk cleanup scheduled",
# #     "User login successful"
# # ]

# # def train_model():
# #     global model, embedder
# #     embedder = SentenceTransformer("all-MiniLM-L6-v2")
# #     X = embedder.encode(sample_logs)
# #     model = IsolationForest(contamination=0.15)
# #     model.fit(X)

# # def is_anomaly(log):
# #     if model is None or embedder is None:
# #         train_model()
# #     vector = embedder.encode([log])
# #     return model.predict(vector)[0] == -1

# # def parse_log_file(path):
# #     train_model()
# #     results = []
# #     with open(path, 'r') as f:
# #         for line in f:
# #             clean = line.strip()
# #             results.append({
# #                 "line": clean,
# #                 "is_malicious": is_anomaly(clean)
# #             })
# #     return results

# from sentence_transformers import SentenceTransformer
# from sklearn.ensemble import IsolationForest

# model = None
# embedder = None

# # Sample safe logs (replace with real logs later)
# normal_logs = [
#     "User login from 192.168.0.1",
#     "Cron job started",
#     "Session opened for user root",
#     "Ping to server successful",
#     "Disk cleanup completed"
# ]

# def train_model():
#     global model, embedder
#     embedder = SentenceTransformer("all-MiniLM-L6-v2")
#     X = embedder.encode(normal_logs)
#     model = IsolationForest(contamination=0.15)
#     model.fit(X)

# def is_anomaly(line):
#     global model, embedder
#     if not model or not embedder:
#         train_model()
#     vector = embedder.encode([line])
#     return model.predict(vector)[0] == -1

# def parse_log_file(path):
#     results = []
#     train_model()
#     with open(path, 'r') as f:
#         for line in f:
#             clean = line.strip()
#             results.append({
#                 "line": clean,
#                 "is_malicious": is_anomaly(clean)
#             })
#     return results



import re  # for regex log parsing
from collections import defaultdict  # to track IP request count
from sentence_transformers import SentenceTransformer  # to embed logs into vectors
from sklearn.ensemble import IsolationForest  # unsupervised anomaly detection
import numpy as np  # fixes JSON serialization bug

# Initialize global model and embedding object
model = None
embedder = None

# Sample known-safe logs to train the model
normal_logs = [
    "User login from 192.168.0.1",
    "Cron job started",
    "Session opened for user root",
    "Ping to server successful",
    "Disk cleanup completed"
]

# Regex pattern to extract log fields like IP, method, path, status code
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>.*?) HTTP/1.1" (?P<status>\d+)'
)

def train_model():
    """
    Trains the IsolationForest model on normal logs using sentence embeddings.
    """
    global model, embedder
    embedder = SentenceTransformer("all-MiniLM-L6-v2")  # Light-weight transformer model
    X = embedder.encode(normal_logs)  # Convert log strings to vectors
    model = IsolationForest(contamination=0.15, random_state=42)  # 15% logs assumed anomalous
    model.fit(X)  # Train on vectorized normal logs

def is_anomaly(text):
    """
    Returns True if the given log line is an AI-detected anomaly.
    """
    global model, embedder
    if not model or not embedder:
        train_model()
    vector = embedder.encode([text])
    return bool(model.predict(vector)[0] == -1)  # Convert np.bool_ to bool to fix JSON bug

def parse_log_file(file_path):
    """
    Parses and analyzes each line of a log file.
    Adds both rule-based and AI-based anomaly detection.
    Returns a list of annotated logs.
    """
    global model, embedder
    train_model()

    ip_count = defaultdict(int)  # Tracks how many requests came from each IP
    parsed_logs = []

    with open(file_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        clean = line.strip()  # Remove extra whitespace

        # Prepare default log structure
        log = {
            "id": i,
            "line": clean,
            "anomaly": False,
            "is_malicious": False,
            "confidence": 0.0,
            "ip": None,
            "status": None,
            "reason": ""
        }

        # Try to parse fields using regex
        match = log_pattern.match(clean)

        if match:
            data = match.groupdict()
            ip = data["ip"]
            status = int(data["status"])
            path = data["path"]

            # Fill in known fields
            log["ip"] = ip
            log["status"] = status
            ip_count[ip] += 1

            # 🚨 Rule 1: Too many requests from the same IP
            if ip_count[ip] > 3:
                log["anomaly"] = True
                log["reason"] = f"High frequency from IP {ip}"
                log["confidence"] = 0.8

            # 🚨 Rule 2: Suspicious access path
            if "/admin" in path or "/wp-login" in path:
                log["anomaly"] = True
                log["reason"] = f"Suspicious path: {path}"
                log["confidence"] = max(log["confidence"], 0.9)

            # 🚨 Rule 3: HTTP status code indicates error
            if status >= 400:
                log["anomaly"] = True
                log["reason"] = f"Returned error status {status}"
                log["confidence"] = max(log["confidence"], 0.7)

        # 🔍 AI-based anomaly detection fallback (even if regex fails)
        log["is_malicious"] = is_anomaly(clean)

        parsed_logs.append(log)

    return parsed_logs

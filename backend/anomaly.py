# import re
# from collections import defaultdict

# # Regex pattern to match each log entry
# log_pattern = re.compile(
#     r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>.*?) HTTP/1.1" (?P<status>\d+)'
# )

# def parse_logs(file_path):
#     ip_count = defaultdict(int)
#     parsed_logs = []

#     with open(file_path, 'r') as f:
#         lines = f.readlines()

#     for i, line in enumerate(lines):
#         line = line.strip()
#         match = log_pattern.match(line)

#         if not match:
#             continue

#         log = match.groupdict()
#         log["id"] = i
#         log["anomaly"] = False
#         log["reason"] = ""
#         log["confidence"] = 0.0

#         ip = log["ip"]
#         status = int(log["status"])
#         path = log["path"]

#         ip_count[ip] += 1

#         # Rule 1: Too many requests from same IP
#         if ip_count[ip] > 3:
#             log["anomaly"] = True
#             log["reason"] = f"High frequency from IP {ip}"
#             log["confidence"] = 0.8

#         # Rule 2: Suspicious path
#         if "/admin" in path or "/wp-login" in path:
#             log["anomaly"] = True
#             log["reason"] = f"Suspicious path: {path}"
#             log["confidence"] = max(log["confidence"], 0.9)

#         # Rule 3: Error codes
#         if status >= 400:
#             log["anomaly"] = True
#             log["reason"] = f"Returned status code {status}"
#             log["confidence"] = max(log["confidence"], 0.7)

#         parsed_logs.append(log)

#     return parsed_logs
import re
from collections import defaultdict

log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>.*?) HTTP/1.1" (?P<status>\d+)'
)

def parse_log_file(file_path):
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

    return parsed_logs

import re  # for regex log parsing
from collections import defaultdict  # to track IP request count
import os

# Regex pattern to extract log fields like IP, method, path, status code
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>.*?) HTTP/1.1" (?P<status>\d+)'
)

# Lightweight suspicious patterns for production
SUSPICIOUS_PATHS = [
    '/admin', '/wp-admin', '/wp-login.php', '/administrator',
    '/phpmyadmin', '/mysql', '/.env', '/config.php', '/backup.sql',
    '/api/admin', '/sensitive', '/secret'
]

SUSPICIOUS_KEYWORDS = [
    'admin', 'login', 'password', 'secret', 'config', 'backup',
    'mysql', 'database', 'env', 'sql', 'dump'
]

def simple_anomaly_check(text):
    """
    Lightweight anomaly detection without ML dependencies.
    Uses keyword matching and pattern recognition.
    """
    text_lower = text.lower()
    
    # Check for suspicious keywords
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text_lower:
            return True
    
    # Check for common attack patterns
    attack_patterns = [
        'script', 'select', 'union', 'drop', 'insert', 'delete',
        '../', '..\\', 'etc/passwd', 'cmd.exe', 'powershell'
    ]
    
    for pattern in attack_patterns:
        if pattern in text_lower:
            return True
    
    return False

def parse_log_file(file_path):
    """
    Production-ready log parser with lightweight anomaly detection.
    Works without heavy ML dependencies.
    """
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
            for suspicious_path in SUSPICIOUS_PATHS:
                if suspicious_path in path:
                    log["anomaly"] = True
                    log["reason"] = f"Suspicious path: {path}"
                    log["confidence"] = max(log["confidence"], 0.9)
                    break

            # 🚨 Rule 3: HTTP status code indicates error
            if status >= 400:
                log["anomaly"] = True
                log["reason"] = f"Returned error status {status}"
                log["confidence"] = max(log["confidence"], 0.7)

        # 🔍 Lightweight anomaly detection fallback
        if simple_anomaly_check(clean):
            log["is_malicious"] = True
            if not log["anomaly"]:  # Don't override rule-based detection
                log["anomaly"] = True
                log["reason"] = "Suspicious content detected"
                log["confidence"] = 0.6

        parsed_logs.append(log)

    return parsed_logs

# Fallback function for when ML libraries aren't available
def is_anomaly_lightweight(text):
    """Simple pattern-based anomaly detection"""
    return simple_anomaly_check(text)

# Production check - use lightweight version if ML imports fail
def get_anomaly_detector():
    """Returns the appropriate anomaly detection function"""
    try:
        # Try to import ML version
        from sentence_transformers import SentenceTransformer
        from sklearn.ensemble import IsolationForest
        
        # If successful, use the full ML version
        from anomaly import is_anomaly as ml_anomaly
        return ml_anomaly
    except ImportError:
        # Fall back to lightweight version
        return is_anomaly_lightweight 
# 📋 Sample Log Files

This folder contains example log files for testing the anomaly detection system.

## 🎯 Files Available

### 1. `example1_normal.log` - Clean Traffic
- **Lines**: 10 entries
- **Content**: Normal website traffic
- **Expected Result**: Few or no anomalies detected

### 2. `example2_suspicious.log` - Attack Simulation  
- **Lines**: 10 entries
- **Content**: Concentrated attack from specific IPs
- **Expected Result**: High anomaly detection rate

### 3. `example3_mixed.log` - Real World Mix
- **Lines**: 15 entries  
- **Content**: Mix of normal and suspicious activity
- **Expected Result**: Moderate anomaly detection

### 4. `example4_realworld.log` - Advanced Patterns
- **Lines**: 27 entries
- **Content**: Advanced attack patterns (WordPress, database hunting, API attacks)
- **Expected Result**: Multiple attack types detected

## 🔍 How to Use

### From Python Code:
```python
from anomaly import parse_log_file

# Test with different sample files
results = parse_log_file('sample_logs/example1_normal.log')
print(f"Found {len([r for r in results if r['anomaly']])} anomalies")
```

### From Web Interface:
1. Start the Flask server: `python app.py`
2. Go to the frontend at `http://localhost:3000`
3. Upload any of these files through the web interface

## 📊 What Each File Tests

- **Rule-based detection**: High frequency, suspicious paths, error codes
- **AI-based detection**: Unusual patterns compared to normal behavior
- **Mixed scenarios**: Real-world complexity with both normal and malicious traffic 
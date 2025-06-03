"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { useAuth } from "../../context/AuthContext";

export default function UploadPage() {
  const { token } = useAuth();
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null); // for selected log file
  const [logs, setLogs] = useState<any[]>([]); // parsed logs
  const [loading, setLoading] = useState(false); // upload loader
  const [stats, setStats] = useState({ total: 0, anomalies: 0, uniqueIPs: 0 }); // summary stats

  // redirect to login if no token
  useEffect(() => {
    if (!token) {
      router.push("/login");
    }
  }, [token]);

  // handle file upload and parsing
  const handleUpload = async () => {
    if (!file || !token) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      const allLogs = res.data.logs;
      setLogs(allLogs);

      // Extract summary stats
      const anomalies = allLogs.filter((log: any) => log.anomaly);
      const uniqueAnomalyIPs = new Set(anomalies.map((log: any) => log.ip));

      setStats({
        total: allLogs.length,
        anomalies: anomalies.length,
        uniqueIPs: uniqueAnomalyIPs.size,
      });
    } catch (err) {
      alert("Upload failed. Please check the file.");
    } finally {
      setLoading(false);
    }
  };

  if (!token) return <p style={{ padding: "2rem" }}>Redirecting to login...</p>;

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Upload Log File</h1>

      {/* File picker + upload button */}
      <div style={styles.uploadBox}>
        <input
          type="file"
          accept=".log,.txt"
          onChange={(e) => {
            if (e.target.files?.[0]) setFile(e.target.files[0]);
          }}
        />
        <button onClick={handleUpload} disabled={loading || !file} style={styles.button}>
          {loading ? "Uploading..." : "Upload"}
        </button>
      </div>

      {/* 📊 Summary stats */}
      {logs.length > 0 && (
        <div style={summaryStyle}>
          <div style={cardStyle}>
            <strong>Total Logs</strong>
            <p>{stats.total}</p>
          </div>
          <div style={cardStyle}>
            <strong>Anomalies</strong>
            <p>🚨 {stats.anomalies}</p>
          </div>
          <div style={cardStyle}>
            <strong>Unique Suspicious IPs</strong>
            <p>{stats.uniqueIPs}</p>
          </div>
        </div>
      )}

      {/* 🧾 Log table */}
      {logs.length > 0 && (
        <div style={{ marginTop: "1rem", overflowX: "auto" }}>
          <h2 style={styles.subheading}>🧾 Log Analysis Result</h2>
          <table style={styles.table}>
            <thead style={styles.thead}>
              <tr>
                <th style={styles.th}>#</th>
                <th style={styles.th}>IP</th>
                <th style={styles.th}>Method</th>
                <th style={styles.th}>Path</th>
                <th style={styles.th}>Status</th>
                <th style={styles.th}>Timestamp</th>
                <th style={styles.th}>Anomaly</th>
                <th style={styles.th}>Reason</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr
                  key={log.id}
                  style={{
                    backgroundColor: log.anomaly
                      ? "var(--row-danger-bg)"
                      : "var(--row-normal-bg)",
                  }}
                >
                  <td style={styles.td}>{log.id}</td>
                  <td style={styles.td}>{log.ip}</td>
                  <td style={styles.td}>{log.method}</td>
                  <td style={styles.td}>{log.path}</td>
                  <td style={styles.td}>
                    <strong
                      style={{
                        color:
                          log.status >= 500
                            ? "darkred"
                            : log.status >= 400
                            ? "orange"
                            : "green",
                      }}
                    >
                      {log.status}
                    </strong>
                  </td>
                  <td style={styles.td}>{log.timestamp}</td>
                  <td style={styles.td}>{log.anomaly ? "🚨 Yes" : "✅ No"}</td>
                  <td style={styles.td}>{log.anomaly ? log.reason : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// ✅ Inline Styles

const styles = {
  container: {
    padding: "2rem",
    fontFamily: "Arial, sans-serif",
    color: "var(--text-color)",
    backgroundColor: "var(--bg-color)",
    minHeight: "100vh",
  },
  heading: {
    fontSize: "24px",
    fontWeight: "bold",
    marginBottom: "1rem",
  },
  subheading: {
    fontSize: "20px",
    fontWeight: 600,
    marginBottom: "1rem",
  },
  uploadBox: {
    display: "flex",
    gap: "1rem",
    alignItems: "center",
    marginBottom: "1rem",
  },
  button: {
    padding: "0.5rem 1rem",
    backgroundColor: "#0070f3",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontWeight: 600,
  },
  table: {
    width: "100%",
    borderCollapse: "collapse" as "collapse",
    fontSize: "14px",
    border: "1px solid #ccc",
  },
  thead: {
    backgroundColor: "var(--header-bg)",
    color: "var(--header-text)",
  },
  th: {
    padding: "10px",
    border: "1px solid #ccc",
    textAlign: "left" as const,
  },
  td: {
    padding: "8px 10px",
    border: "1px solid #ccc",
    color: "var(--text-color)",
  },
};

const summaryStyle = {
  display: "flex",
  gap: "2rem",
  marginTop: "2rem",
  marginBottom: "1rem",
  fontSize: "16px",
};

const cardStyle = {
  padding: "1rem",
  background: "var(--header-bg)",
  border: "1px solid #ccc",
  borderRadius: "8px",
  minWidth: "160px",
  textAlign: "center" as const,
};

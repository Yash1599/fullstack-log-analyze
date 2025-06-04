"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Chart from "chart.js/auto";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";

export default function UploadPage() {
  const { token, isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [filtered, setFiltered] = useState<any[]>([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({ total: 0, anomalies: 0, uniqueIPs: 0 });
  const chartRef = useRef(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (!isAuthenticated) router.push("/login");
  }, [isAuthenticated, router]);

  const handleUpload = async () => {
    if (!file || !token) return;
    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_URL}/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await res.json();
      if (data.error) throw new Error(data.error);

      const allLogs = data.logs || [];
      setLogs(allLogs);
      setFiltered(allLogs);

      const anomalies = allLogs.filter((log: any) => log.is_malicious || log.anomaly);
      const uniqueIPs = new Set(anomalies.map((log: any) => log.ip));

      setStats({
        total: allLogs.length,
        anomalies: anomalies.length,
        uniqueIPs: uniqueIPs.size,
      });

    } catch (err: any) {
      console.error("Upload error:", err);
      setError(err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const applyFilter = (type: string) => {
    setFilter(type);
    if (type === "malicious") {
      setFiltered(logs.filter((log) => log.is_malicious || log.anomaly));
    } else if (type === "safe") {
      setFiltered(logs.filter((log) => !log.is_malicious && !log.anomaly));
    } else {
      setFiltered(logs);
    }
  };

  useEffect(() => {
    if (chartInstance.current) chartInstance.current.destroy();

    if (filtered.length > 0 && chartRef.current) {
      const ctx = chartRef.current as any;
      chartInstance.current = new Chart(ctx, {
        type: "line",
        data: {
          labels: filtered.map((_, i) => `Log ${i + 1}`),
          datasets: [
            {
              label: "Malicious Timeline",
              data: filtered.map((log) => (log.is_malicious || log.anomaly ? 1 : 0)),
              borderColor: "#dc3545",
              backgroundColor: "rgba(220, 53, 69, 0.1)",
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 1,
              ticks: {
                callback: (val) => (val === 1 ? "Malicious" : "Safe"),
              },
            },
          },
        },
      });
    }
  }, [filtered]);

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  if (!isAuthenticated) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: "100vh" }}>
        <div className="text-center">
          <div className="spinner-border text-primary mb-3" role="status" />
          <p>Redirecting...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>🔐 AI Log Analyzer</h2>
        <button className="btn btn-outline-secondary" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="card p-4 shadow-sm mb-4">
        <h5>Upload Log File</h5>
        <input
          type="file"
          className="form-control mb-3"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          disabled={loading}
        />
        <button className="btn btn-primary w-100" onClick={handleUpload} disabled={loading || !file}>
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {logs.length > 0 && (
        <>
          <div className="row mb-4">
            <StatCard title="Total Logs" value={stats.total} bg="primary" />
            <StatCard title="Anomalies" value={stats.anomalies} bg="danger" />
            <StatCard title="Unique IPs" value={stats.uniqueIPs} bg="warning" text="dark" />
          </div>

          <div className="btn-group mb-4 w-100">
            <button className={`btn ${filter === "malicious" ? "btn-danger" : "btn-outline-danger"}`} onClick={() => applyFilter("malicious")}>Malicious</button>
            <button className={`btn ${filter === "safe" ? "btn-success" : "btn-outline-success"}`} onClick={() => applyFilter("safe")}>Safe</button>
            <button className={`btn ${filter === "all" ? "btn-dark" : "btn-outline-dark"}`} onClick={() => applyFilter("all")}>All</button>
          </div>

          <div className="row">
            {filtered.map((log, idx) => (
              <LogCard key={idx} log={log} />
            ))}
          </div>

          <div className="card p-4 mt-5">
            <h5>📊 Timeline</h5>
            <canvas ref={chartRef} />
          </div>
        </>
      )}
    </div>
  );
}

function StatCard({ title, value, bg = "light", text = "white" }: {
  title: string;
  value: number;
  bg?: string;
  text?: string;
}) {
  return (
    <div className="col-md-4">
      <div className={`card text-center bg-${bg} text-${text}`}>
        <div className="card-body">
          <h5 className="card-title">{value}</h5>
          <p className="card-text">{title}</p>
        </div>
      </div>
    </div>
  );
}

function LogCard({ log }: {
  log: {
    anomaly?: boolean;
    is_malicious?: boolean;
    confidence?: number;
    line: string;
    reason?: string;
    ip: string;
    status: string;
  };
}) {
  return (
    <div className="col-md-6 mb-3">
      <div className={`card shadow-sm p-3 border-${log.anomaly ? "danger" : "success"}`}>
        <div className="d-flex justify-content-between">
          <span className={`badge ${log.anomaly ? "bg-danger" : "bg-success"}`}>
            {log.anomaly ? "🚨 Malicious" : "✅ Safe"}
          </span>
          {log.confidence && (
            <small className="text-muted">Confidence: {(log.confidence * 100).toFixed(1)}%</small>
          )}
        </div>
        <p className="small font-monospace mt-2">{log.line}</p>
        {log.reason && (
          <div className="alert alert-warning p-1 mt-2">
            <strong>Reason:</strong> {log.reason}
          </div>
        )}
        <div className="row text-muted small mt-2">
          <div className="col">IP: {log.ip}</div>
          <div className="col">Status: {log.status}</div>
        </div>
      </div>
    </div>
  );
}

"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/AuthContext";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

// API URL from environment variable, fallback to localhost for development
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";

export default function LoginPage() {
  const { setToken, setUser } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

const handleLogin = async () => {
  try {
    const res = await axios.post(`${API_URL}/login`, {
      username,
      password,
    });

    if (res.data?.token) {
      setToken(res.data.token);        // Save token using context
      setUser(username);               // Save username as user
      router.push("/upload");          // ✅ Redirect
    } else {
      setError("Login failed. No token returned.");
    }

  } catch (err: any) {
    if (err.response?.data?.error) {
      setError(err.response.data.error);
    } else {
      setError("Login failed. Server not reachable.");
    }
  }
};


  return (
    <div className="d-flex align-items-center justify-content-center vh-100 bg-dark text-white">
      <div className="card p-4 shadow-lg" style={{ width: "400px" }}>
        <h3 className="text-center mb-3">🔐 Log In</h3>
        {error && <div className="alert alert-danger">{error}</div>}
        <input
          className="form-control mb-3"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="form-control mb-3"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="btn btn-primary w-100 mb-2" onClick={handleLogin}>
          Login
        </button>
        <button className="btn btn-link text-center" onClick={() => router.push("/signup")}>
          Don't have an account? Sign up
        </button>
      </div>
    </div>
  );
}

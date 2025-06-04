// "use client";

// import { useState } from "react";
// import axios from "axios";
// import { useRouter } from "next/navigation";
// import { useAuth } from "../../context/AuthContext";
// import Link from "next/link";

// // API URL from environment variable, fallback to localhost for development
// const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";

// export default function SignupPage() {
//   const { setToken } = useAuth();
//   const [formData, setFormData] = useState({
//     fullName: "",
//     email: "",
//     username: "",
//     password: "",
//     confirmPassword: "",
//   });
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");
//   const [acceptTerms, setAcceptTerms] = useState(false);
//   const router = useRouter();

//   const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     setFormData({
//       ...formData,
//       [e.target.name]: e.target.value,
//     });
//   };

//   const isFormValid = () => {
//     return (
//       formData.fullName.trim() &&
//       formData.email.trim() &&
//       formData.username.trim() &&
//       formData.password.trim() &&
//       formData.confirmPassword.trim() &&
//       acceptTerms
//     );
//   };

//   const handleSignup = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);
//     setError("");

//     // Validation
//     if (formData.password !== formData.confirmPassword) {
//       setError("Passwords do not match");
//       setLoading(false);
//       return;
//     }

//     if (formData.password.length < 8) {
//       setError("Password must be at least 8 characters long");
//       setLoading(false);
//       return;
//     }

//     if (!acceptTerms) {
//       setError("Please accept the Terms and Conditions");
//       setLoading(false);
//       return;
//     }

//     try {
//       // For demo purposes, we'll simulate a signup API call
//       // In a real app, you'd call your signup endpoint
//       console.log("Signup data:", formData);
      
//       // Simulate API delay
//       await new Promise(resolve => setTimeout(resolve, 1500));
      
//       // For now, redirect to login page with success message
//       router.push("/login?message=Account created successfully! Please sign in.");
      
//     } catch (err: any) {
//       setError(err.response?.data?.error || "Signup failed. Please try again.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="auth-container">
//       <div className="auth-card">
//         {/* Header */}
//         <div className="text-center mb-4">
//           <i className="bi bi-person-plus" style={{ 
//             fontSize: "clamp(2.5rem, 6vw, 3rem)", 
//             color: "white", 
//             marginBottom: "clamp(16px, 4vw, 20px)",
//             display: "block"
//           }}></i>
//           <h1 className="auth-title">Create Account</h1>
//           <p className="auth-subtitle">Join Log Analyzer to get started with anomaly detection</p>
//         </div>

//         {/* Error Message */}
//         {error && (
//           <div className="error-message">
//             <i className="bi bi-exclamation-triangle me-2"></i>
//             {error}
//           </div>
//         )}

//         {/* Signup Form */}
//         <form onSubmit={handleSignup} noValidate>
//           <div className="form-floating">
//             <input
//               type="text"
//               className="form-control"
//               id="fullName"
//               name="fullName"
//               placeholder="Enter your full name"
//               value={formData.fullName}
//               onChange={handleInputChange}
//               required
//               autoComplete="name"
//               autoFocus
//             />
//             <label htmlFor="fullName">
//               <i className="bi bi-person"></i>Full Name
//             </label>
//           </div>

//           <div className="form-floating">
//             <input
//               type="email"
//               className="form-control"
//               id="email"
//               name="email"
//               placeholder="Enter your email address"
//               value={formData.email}
//               onChange={handleInputChange}
//               required
//               autoComplete="email"
//             />
//             <label htmlFor="email">
//               <i className="bi bi-envelope"></i>Email Address
//             </label>
//           </div>

//           <div className="form-floating">
//             <input
//               type="text"
//               className="form-control"
//               id="username"
//               name="username"
//               placeholder="Choose a username"
//               value={formData.username}
//               onChange={handleInputChange}
//               required
//               autoComplete="username"
//             />
//             <label htmlFor="username">
//               <i className="bi bi-at"></i>Username
//             </label>
//           </div>

//           <div className="form-floating">
//             <input
//               type="password"
//               className="form-control"
//               id="password"
//               name="password"
//               placeholder="Create a strong password"
//               value={formData.password}
//               onChange={handleInputChange}
//               required
//               autoComplete="new-password"
//               minLength={8}
//             />
//             <label htmlFor="password">
//               <i className="bi bi-lock"></i>Password (min. 8 characters)
//             </label>
//           </div>

//           <div className="form-floating">
//             <input
//               type="password"
//               className="form-control"
//               id="confirmPassword"
//               name="confirmPassword"
//               placeholder="Confirm your password"
//               value={formData.confirmPassword}
//               onChange={handleInputChange}
//               required
//               autoComplete="new-password"
//               minLength={8}
//             />
//             <label htmlFor="confirmPassword">
//               <i className="bi bi-lock-fill"></i>Confirm Password
//             </label>
//           </div>

//           {/* Terms and Conditions */}
//           <div className="form-check mb-4">
//             <input 
//               className="form-check-input" 
//               type="checkbox" 
//               id="acceptTerms"
//               checked={acceptTerms}
//               onChange={(e) => setAcceptTerms(e.target.checked)}
//             />
//             <label className="form-check-label text-white-50" htmlFor="acceptTerms">
//               I agree to the{" "}
//               <Link href="/terms" className="auth-link">
//                 Terms and Conditions
//               </Link>{" "}
//               and{" "}
//               <Link href="/privacy" className="auth-link">
//                 Privacy Policy
//               </Link>
//             </label>
//           </div>

//           <button 
//             type="submit" 
//             className="auth-btn mb-4"
//             disabled={loading || !isFormValid()}
//           >
//             {loading ? (
//               <>
//                 <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
//                 <span>Creating account...</span>
//               </>
//             ) : (
//               <>
//                 <i className="bi bi-check-circle"></i>
//                 <span>Create Account</span>
//               </>
//             )}
//           </button>
//         </form>

//         {/* Divider */}
//         <div className="auth-divider">
//           <span>or sign up with</span>
//         </div>

//         {/* Social Signup Buttons */}
//         <div className="row g-2 mb-4">
//           <div className="col-6">
//             <button type="button" className="social-btn" title="Sign up with Google">
//               <i className="bi bi-google"></i>
//               <span className="d-none d-sm-inline">Google</span>
//             </button>
//           </div>
//           <div className="col-6">
//             <button type="button" className="social-btn" title="Sign up with GitHub">
//               <i className="bi bi-github"></i>
//               <span className="d-none d-sm-inline">GitHub</span>
//             </button>
//           </div>
//         </div>

//         {/* Login Link */}
//         <div className="text-center mb-4">
//           <span className="text-white-50">Already have an account? </span>
//           <Link href="/login" className="auth-link fw-bold">
//             Sign in here
//           </Link>
//         </div>

//         {/* Security Note */}
//         <div className="info-card">
//           <div className="text-center">
//             <small className="text-white-50">
//               <i className="bi bi-shield-check me-2"></i>
//               Your data is secure and encrypted with industry-standard protection
//             </small>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// } 



"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import "bootstrap/dist/css/bootstrap.min.css";

export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSignup = async () => {
    const res = await fetch("http://localhost:10000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    if (res.ok) {
      setMessage("Signup successful! Please login.");
      setTimeout(() => router.push("/login"), 2000);
    } else {
      setError(data.error || "Signup failed");
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100 bg-secondary text-white">
      <div className="card p-4 shadow-lg" style={{ width: "400px" }}>
        <h3 className="text-center mb-3">📝 Sign Up</h3>
        {message && <div className="alert alert-success">{message}</div>}
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
        <button className="btn btn-success w-100 mb-2" onClick={handleSignup}>
          Sign Up
        </button>
        <button className="btn btn-link text-center" onClick={() => router.push("/login")}>
          Already have an account? Login
        </button>
      </div>
    </div>
  );
}

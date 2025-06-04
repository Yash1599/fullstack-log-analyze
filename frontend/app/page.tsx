import Link from "next/link";

export default function Home() {
  return (
    <div className="auth-container">
      <div className="auth-card">
        {/* Header */}
        <div className="text-center mb-4">
          <i className="bi bi-graph-up-arrow" style={{ fontSize: "clamp(3rem, 8vw, 4rem)", color: "white", marginBottom: "clamp(16px, 4vw, 20px)", display: "block" }}></i>
          <h1 className="auth-title">Log Analyzer</h1>
          <p className="auth-subtitle">Advanced cybersecurity log analysis with AI-powered anomaly detection</p>
        </div>

        {/* Features */}
        <div className="row g-3 mb-4">
          <div className="col-12 col-md-4">
            <div className="feature-card">
              <i className="bi bi-shield-check"></i>
              <h5 className="text-white">Secure Analysis</h5>
              <small className="text-white-50">Advanced security protocols</small>
            </div>
          </div>
          <div className="col-12 col-md-4">
            <div className="feature-card">
              <i className="bi bi-cpu"></i>
              <h5 className="text-white">AI Detection</h5>
              <small className="text-white-50">Rule-based anomaly detection</small>
            </div>
          </div>
          <div className="col-12 col-md-4">
            <div className="feature-card">
              <i className="bi bi-speedometer2"></i>
              <h5 className="text-white">Real-time</h5>
              <small className="text-white-50">Instant log processing</small>
            </div>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="d-grid gap-3 mb-4">
          <Link href="/login" className="auth-btn text-decoration-none">
            <i className="bi bi-box-arrow-in-right"></i>
            <span>Sign In to Your Account</span>
          </Link>
          
          <Link href="/signup" className="social-btn text-decoration-none text-center">
            <i className="bi bi-person-plus"></i>
            <span>Create New Account</span>
          </Link>
        </div>

        {/* Demo Information */}
        <div className="info-card">
          <div className="text-center">
            <small className="text-white-50">
              <i className="bi bi-info-circle me-2"></i>
              Try the demo with credentials:
            </small>
            <div className="mt-2">
              <small className="text-white">
                <strong>Username:</strong> admin<br/>
                <strong>Password:</strong> password123
              </small>
            </div>
          </div>
        </div>

        {/* Key Features List */}
        <div className="features-list">
          <h6 className="text-white text-center mb-3">What you can do:</h6>
          <div className="row g-2">
            <div className="col-6">
              <div className="feature-item">
                <i className="bi bi-check-circle-fill text-success"></i>
                <small className="text-white-50">Upload log files</small>
              </div>
            </div>
            <div className="col-6">
              <div className="feature-item">
                <i className="bi bi-check-circle-fill text-success"></i>
                <small className="text-white-50">Detect anomalies</small>
              </div>
            </div>
            <div className="col-6">
              <div className="feature-item">
                <i className="bi bi-check-circle-fill text-success"></i>
                <small className="text-white-50">View analytics</small>
              </div>
            </div>
            <div className="col-6">
              <div className="feature-item">
                <i className="bi bi-check-circle-fill text-success"></i>
                <small className="text-white-50">Export reports</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

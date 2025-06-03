# Fullstack Log Analyzer

A web application for analyzing server logs and detecting anomalies using rule-based AI models. The application consists of a Flask backend for log processing and anomaly detection, and a Next.js frontend for visualization and user interaction.

## Features

- **Log File Upload**: Upload server log files for analysis
- **Anomaly Detection**: Automated detection of suspicious activities using rule-based algorithms
- **Real-time Visualization**: Interactive charts and dashboards using Chart.js
- **Authentication**: JWT-based authentication system
- **Modern UI**: Responsive design built with Next.js and Tailwind CSS

## Technology Stack

### Backend
- **Flask**: Python web framework
- **Python**: Core language for log processing and anomaly detection
- **JWT**: JSON Web Tokens for authentication
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **Next.js 15**: React framework with App Router
- **React 19**: Frontend library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Data visualization library
- **Axios**: HTTP client for API requests

## Prerequisites

Make sure you have the following installed on your system:

- **Node.js** (v18 or higher)
- **npm** or **yarn**
- **Python** (v3.8 or higher)
- **pip** (Python package manager)

## Local Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fullstack-log-analyzer
```

### 2. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
# or
yarn install
```

### 4. Running the Application

#### Start the Backend Server

From the `backend` directory:

```bash
python app.py
```

The Flask server will start on `http://localhost:10000`

#### Start the Frontend Development Server

From the `frontend` directory:

```bash
npm run dev
# or
yarn dev
```

The Next.js development server will start on `http://localhost:3000`

### 5. Access the Application

1. Open your browser and navigate to `http://localhost:3000`
2. Log in using the default credentials:
   - **Username**: `admin`
   - **Password**: `password123`
3. Upload a log file to begin analysis

## Anomaly Detection Approach

The application uses a **rule-based anomaly detection system** that analyzes server logs to identify suspicious activities. The AI model is implemented in `backend/anomaly.py` and employs the following detection strategies:

### Log Parsing
- Uses regex pattern matching to parse Common Log Format (CLF) entries
- Extracts key components: IP address, timestamp, HTTP method, path, and status code

### Detection Rules

#### 1. High Frequency Requests (Confidence: 0.8)
**Rule**: Flags IPs making more than 3 requests
**Purpose**: Detect potential DDoS attacks or automated scraping
**Implementation**: Maintains a counter for each IP address

#### 2. Suspicious Path Access (Confidence: 0.9)
**Rule**: Identifies access to sensitive endpoints
**Patterns Detected**:
- `/admin` - Administrative interfaces
- `/wp-login` - WordPress login attempts
**Purpose**: Detect unauthorized access attempts or reconnaissance

#### 3. HTTP Error Codes (Confidence: 0.7)
**Rule**: Flags responses with status codes ≥ 400
**Common Cases**:
- 404 (Not Found) - Potential scanning attempts
- 401/403 (Unauthorized/Forbidden) - Access violations
- 500+ (Server Errors) - System issues
**Purpose**: Identify failed requests that may indicate attacks or system problems

### Confidence Scoring
Each anomaly is assigned a confidence score (0.0-1.0) based on the severity and reliability of the detection rule. Multiple rules can apply to a single log entry, with the highest confidence score being retained.

### Output Format
For each log entry, the system provides:
- **Anomaly Status**: Boolean flag indicating if the entry is anomalous
- **Reason**: Human-readable explanation of why it was flagged
- **Confidence**: Numerical score representing detection confidence
- **Parsed Fields**: Structured data extracted from the log entry

## Log File Format

The application expects server logs in Common Log Format (CLF):

```
192.168.1.100 - - [10/Oct/2000:13:55:36 +0000] "GET /index.html HTTP/1.1" 200
```

## API Endpoints

### Authentication
- `POST /login` - User authentication
- Requires: `{"username": "string", "password": "string"}`
- Returns: JWT token

### Log Analysis
- `POST /upload` - Upload and analyze log files
- Requires: JWT token in Authorization header
- Returns: Parsed logs with anomaly detection results

## Development

### Backend Development
- Log processing logic: `backend/anomaly.py`
- Main application: `backend/app.py`
- Add new detection rules by modifying the parsing logic in `anomaly.py`

### Frontend Development
- Main application code: `frontend/app/`
- Components and context: `frontend/context/`
- Styling with Tailwind CSS classes

## Security Considerations

- JWT tokens expire after 1 hour
- File uploads are restricted to authenticated users
- CORS is configured for local development

## Future Enhancements

- **Machine Learning Models**: Implement unsupervised learning algorithms (Isolation Forest, One-Class SVM)
- **Time-Series Analysis**: Add temporal pattern detection
- **Behavioral Analysis**: User session and behavior profiling
- **Real-time Processing**: WebSocket integration for live log monitoring
- **Advanced Visualization**: Geolocation mapping, network topology views
- **Alert System**: Email/SMS notifications for critical anomalies

## Troubleshooting

### Common Issues

1. **Backend not starting**: Ensure Python dependencies are installed
2. **Frontend build errors**: Clear node_modules and reinstall dependencies
3. **Authentication issues**: Check if backend is running on port 10000
4. **File upload failures**: Verify JWT token is valid and not expired

### Logs and Debugging
- Backend logs are printed to console
- Frontend development server provides detailed error messages
- Check browser console for client-side errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 
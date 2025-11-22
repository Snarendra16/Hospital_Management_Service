# Hospital Management System

## Prerequisites
- Python 3.8+
- Node.js 16+
- Redis (Running on localhost:6379)

## Setup

1. **Backend Setup**
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```

2. **Frontend Setup**
   ```powershell
   cd frontend
   npm install
   ```

## Running the Application

You can use the provided `run_app.ps1` script or run the components manually.

### Manual Start

1. **Start Redis** (Ensure it's running)

2. **Start Celery Worker** (In backend folder)
   ```powershell
   celery -A app.celery worker --loglevel=info --pool=solitaire
   ```
   *Note: On Windows, `--pool=solitaire` or `--pool=solo` is often required.*

3. **Start Flask Backend** (In backend folder)
   ```powershell
   python app.py
   ```

4. **Start Vue Frontend** (In frontend folder)
   ```powershell
   npm run dev
   ```

## Default Credentials
- **Admin**: username: `admin`, password: `admin123`
# Hospital_Management_Service

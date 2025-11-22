# Start Backend
Start-Process -FilePath "cmd" -ArgumentList "/k cd backend && python app.py" -WindowStyle Normal

# Start Frontend
Start-Process -FilePath "cmd" -ArgumentList "/k cd frontend && npm run dev" -WindowStyle Normal

# Start Celery (Optional, uncomment if Redis is running)
# Start-Process -FilePath "cmd" -ArgumentList "/k cd backend && celery -A app.celery worker --loglevel=info --pool=solo" -WindowStyle Normal

Write-Host "HMS Started! Backend on http://localhost:5000, Frontend on http://localhost:5173"

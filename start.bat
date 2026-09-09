@echo off
TITLE MahaArogya Setu Launcher
echo ===================================================
echo   Starting MahaArogya Setu (FastAPI + Next.js)
echo ===================================================

echo [1/2] Launching FastAPI Backend on port 8000...
start "MahaArogya Backend (Port 8000)" cmd /k ".\venv\Scripts\uvicorn.exe api:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Launching Next.js Frontend on port 3000...
cd frontend
start "MahaArogya Frontend (Port 3000)" cmd /k "npm run dev"

echo.
echo Both servers started!
echo Frontend UI : http://localhost:3000
echo Backend API : http://localhost:8000
echo ===================================================
pause

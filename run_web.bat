@echo off
echo.
echo ======================================================================
echo   Starting Web Review Predictor...
echo ======================================================================
echo.
echo   Opening browser at http://localhost:8080
echo   Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
start http://localhost:8080
".venv\Scripts\python.exe" web_predictor.py

pause

@echo off
echo.
echo ======================================================================
echo   Starting Advanced Review Predictor...
echo ======================================================================
echo.

cd /d "%~dp0"
".venv\Scripts\python.exe" predict_review.py

pause

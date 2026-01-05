@echo off
echo.
echo ======================================================================
echo   Starting Simple Review Predictor...
echo ======================================================================
echo.

cd /d "%~dp0"
".venv\Scripts\python.exe" simple_predict.py

pause

@echo off
color 0A
title Fake Review Detector - HTML Version

echo.
echo ======================================================================
echo   Opening Fake Review Detector (Offline HTML Version)
echo ======================================================================
echo.
echo   - No server needed!
echo   - Works offline
echo   - Opens in your default browser
echo.

start "" "%~dp0review_detector.html"

echo   Browser opened with review detector page!
echo.
echo   Enjoy testing your reviews!
echo ======================================================================
echo.

timeout /t 3 >nul

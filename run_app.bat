@echo off
REM License Plate Information System Launcher
REM Double-click this file to start the application

echo Starting License Plate Information System...
cd /d "%~dp0"
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Failed to start the application.
    echo Please make sure Python is installed and in your PATH.
    echo.
    pause
)
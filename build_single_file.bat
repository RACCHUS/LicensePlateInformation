@echo off
REM Build Script for License Plate Information System - SINGLE FILE VERSION
REM Creates a single executable file

echo ========================================
echo License Plate Info - Single File Build
echo ========================================
echo.
echo NOTE: This creates a single .exe file
echo Slower startup but easier to distribute
echo.

REM Check if PyInstaller is installed
echo Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo PyInstaller installed successfully!
    echo.
) else (
    echo PyInstaller is already installed.
    echo.
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Previous builds cleaned.
echo.

REM Build the application
echo Building application (Single File Mode)...
echo This will take longer than directory mode...
echo.
pyinstaller LicensePlateInfo_SingleFile.spec

if errorlevel 1 (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo Check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Output location: dist\LicensePlateInfo.exe
echo File size: (check dist folder)
echo.
echo To run: dist\LicensePlateInfo.exe
echo.
echo To distribute: Send the single .exe file
echo.
echo NOTE: First run will be slower as it extracts files
echo.

REM Ask if user wants to test
set /p test="Test the application now? (y/n): "
if /i "%test%"=="y" (
    echo.
    echo Starting application...
    echo (First run may be slow)
    start "" "dist\LicensePlateInfo.exe"
)

echo.
echo Press any key to exit...
pause >nul

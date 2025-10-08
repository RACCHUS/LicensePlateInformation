@echo off
REM Build Script for License Plate Information System
REM Creates a directory-based distribution (RECOMMENDED)

echo ========================================
echo License Plate Info - Build Script
echo ========================================
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
echo Building application (Directory Mode)...
echo This will take a few minutes...
echo.
pyinstaller LicensePlateInfo.spec

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
echo Output location: dist\LicensePlateInfo\
echo Main executable: dist\LicensePlateInfo\LicensePlateInfo.exe
echo.
echo To run: cd dist\LicensePlateInfo && LicensePlateInfo.exe
echo.
echo To distribute: ZIP the entire "LicensePlateInfo" folder
echo.

REM Ask if user wants to test
set /p test="Test the application now? (y/n): "
if /i "%test%"=="y" (
    echo.
    echo Starting application...
    start "" "dist\LicensePlateInfo\LicensePlateInfo.exe"
)

echo.
echo Press any key to exit...
pause >nul

@echo off
REM Build Script for License Plate Information System (PySide6 Version)
REM Creates a directory-based distribution

echo ========================================
echo License Plate Info - PySide6 Build Script
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

REM Check if PySide6 is installed
echo Checking for PySide6...
python -m pip show PySide6 >nul 2>&1
if errorlevel 1 (
    echo PySide6 not found. Installing...
    python -m pip install PySide6
    if errorlevel 1 (
        echo ERROR: Failed to install PySide6
        pause
        exit /b 1
    )
    echo PySide6 installed successfully!
    echo.
) else (
    echo PySide6 is already installed.
    echo.
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Previous builds cleaned.
echo.

REM Build the application
echo Building PySide6 application (Directory Mode)...
echo This will take a few minutes...
echo.
pyinstaller LicensePlateInfo_PySide6.spec

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
echo Run: dist\LicensePlateInfo\LicensePlateInfo.exe
echo.
echo NOTE: This is the PySide6 version with improved DPI scaling
echo.

pause

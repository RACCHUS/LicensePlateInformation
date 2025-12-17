@echo off
REM Cleanup Script - Removes files not needed for distribution
REM Run this BEFORE building the executable to reduce size

echo ========================================
echo License Plate Info - Cleanup Script
echo ========================================
echo.
echo This will remove development files:
echo - Python cache (__pycache__)
echo - Test files
echo - Git files
echo - VS Code settings
echo.
echo ⚠️  WARNING: This is permanent!
echo ⚠️  Make sure you have a backup!
echo.

set /p confirm="Continue with cleanup? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Starting cleanup...
echo.

REM Remove Python cache
echo Removing Python cache files...
if exist __pycache__ rmdir /s /q __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo ✓ Python cache cleaned

REM Remove pytest cache
echo Removing pytest cache...
if exist .pytest_cache rmdir /s /q .pytest_cache
echo ✓ Pytest cache cleaned

REM Remove VS Code settings (optional)
set /p vscode="Remove VS Code settings? (y/n): "
if /i "%vscode%"=="y" (
    if exist .vscode rmdir /s /q .vscode
    echo ✓ VS Code settings removed
)

REM Remove Git files (optional - BE CAREFUL!)
set /p git="Remove Git repository? (y/n): "
if /i "%git%"=="y" (
    if exist .git rmdir /s /q .git
    if exist .gitignore del .gitignore
    echo ✓ Git files removed
)

REM Clean build artifacts
echo Removing build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec 2>nul
echo ✓ Build artifacts cleaned

REM Remove test files (optional)
set /p tests="Remove test files? (y/n): "
if /i "%tests%"=="y" (
    if exist tests rmdir /s /q tests
    echo ✓ Test files removed
)

REM data/pending was already removed during folder consolidation
echo ✓ data/pending/ already removed (saved ~500 MB)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Your project is now ready for building.
echo.
echo Next steps:
echo 1. Run build.bat (for directory distribution)
echo    OR
echo    Run build_single_file.bat (for single exe)
echo.
echo 2. Test the executable
echo 3. Package for distribution
echo.

pause

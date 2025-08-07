@echo off
echo.
echo ========================================
echo   Bazaraki Deal Finder - Windows Setup
echo ========================================
echo.

REM Try to find Python
set PYTHON_CMD=

REM Method 1: Try python command
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    echo ✅ Found Python via 'python' command
    goto :found_python
)

REM Method 2: Try py launcher
py -3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py -3
    echo ✅ Found Python via 'py -3' launcher
    goto :found_python
)

REM Method 3: Try python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    echo ✅ Found Python via 'python3' command
    goto :found_python
)

REM Python not found
echo ❌ Python not found!
echo.
echo Please install Python from: https://www.python.org/downloads/
echo ⚠️  IMPORTANT: Check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:found_python
echo Python command: %PYTHON_CMD%
echo.

REM Check if windows_setup.py exists
if not exist "windows_setup.py" (
    echo ❌ windows_setup.py not found!
    echo Make sure you're in the correct directory with all the files.
    echo.
    pause
    exit /b 1
)

REM Run Windows setup
echo 🚀 Running Windows setup...
echo.
%PYTHON_CMD% windows_setup.py

REM Check if setup was successful
if %errorlevel% == 0 (
    echo.
    echo ✅ Setup completed successfully!
    echo.
    echo 🎯 Next steps:
    echo 1. Double-click "start_bazaraki.bat" to launch the scraper
    echo 2. Or run: %PYTHON_CMD% run_scraper.py
    echo.
) else (
    echo.
    echo ❌ Setup failed. Please check the errors above.
    echo.
    echo 🔧 Try these manual commands:
    echo %PYTHON_CMD% -m pip install --upgrade pip
    echo %PYTHON_CMD% -m pip install requests beautifulsoup4 pandas selenium webdriver-manager lxml openpyxl
    echo.
)

echo Press any key to continue...
pause >nul
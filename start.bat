@echo off
echo.
echo ================================
echo  Vortex Web IDE Startup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

REM Check if Vortex parser exists
if not exist "..\Vortex-Programming-Language\python_parser" (
    echo.
    echo [WARNING] Vortex parser not found in expected location
    echo Expected: ..\Vortex-Programming-Language\python_parser
    echo Please ensure the Vortex-Programming-Language directory is in the parent folder
    echo.
)

REM Start the server
echo.
echo ================================
echo  Starting Flask Server
echo ================================
echo.
echo Server URL: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause

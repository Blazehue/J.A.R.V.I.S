@echo off
echo ================================================
echo   JARVIS V2 - Installation Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Python found
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo.

REM Activate virtual environment and install dependencies
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Warning: Some packages failed to install
    echo This is normal for optional dependencies like pywin32
    echo.
)
echo.

REM Create config if it doesn't exist
echo [4/5] Setting up configuration...
if exist config\config.json (
    echo Configuration file already exists
) else (
    copy config\config.example.json config\config.json
    echo Configuration file created
)
echo.

REM Create necessary directories
echo [5/5] Creating directories...
if not exist logs mkdir logs
if not exist screenshots mkdir screenshots
echo.

echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo To start Jarvis, run:
echo   1. Activate environment: venv\Scripts\activate
echo   2. Run Jarvis: python main.py
echo.
echo Or simply run: run_jarvis.bat
echo.
echo For CLI mode: python main.py --mode cli
echo For voice mode: python main.py --mode voice
echo.
echo See QUICKSTART.md for more information
echo.
pause

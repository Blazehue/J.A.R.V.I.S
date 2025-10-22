@echo off
echo Starting Jarvis V2...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python main.py %*

if %errorlevel% neq 0 (
    echo.
    echo Jarvis encountered an error
    pause
)

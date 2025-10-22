@echo off
echo Running Jarvis V2 Tests...
echo.

if not exist venv (
    echo Virtual environment not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python test_jarvis.py
pause

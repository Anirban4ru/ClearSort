@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3 -m venv .venv
    ) else (
        where python >nul 2>&1
        if errorlevel 1 (
            echo Python 3 was not found. Install Python from https://www.python.org/downloads/
            pause
            exit /b 1
        )
        python -m venv .venv
    )
    if errorlevel 1 (
        echo Failed to create the project virtual environment.
        pause
        exit /b 1
    )
)

.venv\Scripts\python.exe -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install required packages.
        pause
        exit /b 1
    )
)

.venv\Scripts\python.exe main.py
if errorlevel 1 (
    echo.
    echo ClearSort stopped with an error.
    pause
)

endlocal

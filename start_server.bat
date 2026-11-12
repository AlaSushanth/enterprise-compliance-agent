@echo off
setlocal enabledelayedexpansion
title AEGIS-OPERATOR Multi-Agent Pod
echo ======================================================================
echo   Starting AEGIS-OPERATOR Multi-Agent Compliance Engine...
echo ======================================================================

cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

:: Locate python executable
set PY_CMD=python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if !errorlevel! equ 0 (
        set PY_CMD=py
    ) else (
        if exist "C:\Users\suman\AppData\Local\Programs\Python\Python311\python.exe" (
            set PY_CMD="C:\Users\suman\AppData\Local\Programs\Python\Python311\python.exe"
        ) else (
            echo [ERROR] Python not found. Please ensure Python is installed and in your PATH.
            pause
            exit /b 1
        )
    )
)

echo [+] Using Python: %PY_CMD%
echo [+] Starting server on http://localhost:8080 ...

:: Launch browser in background after 2 seconds
start "" powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8080'"

:: Start FastAPI server
%PY_CMD% run.py

pause

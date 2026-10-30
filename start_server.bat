@echo off
title AEGIS-OPERATOR Multi-Agent Pod
echo ======================================================================
echo   Starting AEGIS-OPERATOR Enterprise Multi-Agent Pod...
echo ======================================================================
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
start http://localhost:8000
python run.py
pause

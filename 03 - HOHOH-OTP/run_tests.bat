@echo off
echo ================================
echo Running HOHOH-OTP Test Suite
echo ================================
cd /d "%~dp0"
python -m pytest
pause


@echo off
title KisanSAATHI 2.0 - Your Digital Krishi Officer
color 0A

echo =====================================================================
echo              KisanSAATHI 2.0 - Smart AgriTech SaaS
echo                   Your Digital Krishi Officer
echo =====================================================================
echo.

:: Change directory to current script directory
cd /d "%~dp0"

:: Check for Python
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=py
    goto :PYTHON_FOUND
)

where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python
    goto :PYTHON_FOUND
)

echo [ERROR] Python 3.12+ was not found on your PATH!
echo Please install Python 3.12+ or add it to your Windows Environment Variables.
pause
exit /b 1

:PYTHON_FOUND
echo [*] Using Python executable: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: Verify database migrations
echo [*] Checking database migrations...
%PYTHON_CMD% manage.py migrate --noinput
if %ERRORLEVEL% neq 0 (
    echo [!] Warning: Database migration failed. Continuing...
)

:: Seed demo data if database is fresh
if not exist "db.sqlite3" (
    echo [*] New database detected. Seeding realistic agricultural demonstration data...
    %PYTHON_CMD% scripts\seed_demo_data.py
)

echo.
echo =====================================================================
echo   Platform URLs:
echo   - Home Portal:      http://127.0.0.1:8000/
echo   - Mandi Prices:     http://127.0.0.1:8000/markets/
echo   - Net Calculator:   http://127.0.0.1:8000/calculator/
echo   - AI Crop Wellness: http://127.0.0.1:8000/wellness/
echo   - Grounded AI Chat: http://127.0.0.1:8000/assistant/
echo   - Web3 Trust Ledger:http://127.0.0.1:8000/ledger/verify/?code=KS-REC-2026-X0001
echo.
echo   Demo Login Accounts:
echo   - Farmer:   ramesh_karnal / farmer123
echo   - Buyer:    shiva_agro    / buyer123
echo   - FPO:      fpo_samriddhi / fpo123
echo   - Admin:    admin         / admin123
echo =====================================================================
echo.
echo [*] Launching web browser in 3 seconds...
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:8000/"

echo [*] Starting Django Development Server on http://127.0.0.1:8000/ ...
echo [*] Press Ctrl+C to stop the server.
echo.
%PYTHON_CMD% manage.py runserver 127.0.0.1:8000

echo.
echo Server stopped.
pause

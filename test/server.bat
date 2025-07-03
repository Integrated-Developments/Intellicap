:: filepath: c:\.Repo\Intellicap\test\server.bat
@echo off
:: Self-elevate to admin
:: (If not running as admin, relaunch self as admin)
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Clear the terminal
cls

:: Start Flask app (adjust path as needed)
start "" "%SystemRoot%\System32\cmd.exe" /k "python C:\.Repo\Intellicap\core\flask\run.py"

:: Wait a few seconds for Flask to start
timeout /t 3 /nobreak >nul

:: Start cloudflared tunnel
start "" "%SystemRoot%\System32\cmd.exe" /k "cloudflared tunnel run flask"

:: Optional: Keep window open
pause

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

wsl.exe -d Ubuntu -- bash -c code-server

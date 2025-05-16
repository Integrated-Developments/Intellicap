:: Version 0.0.5

@ echo off
echo ==================================================
echo 	WARNING: Are you sure you want to run setup?
echo ==================================================
pause

:: Ensure we're in the project directory
cd /d "%~dp0..\"
echo [INFO] Changed directory to %CD%

echo ==================================================
echo 	WARNING: Is %CD% the correct Directory?
echo ==================================================
pause

:: Check if virtual environment exists, create if not
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Virtual environment creation failed! Exiting...
        pause
        exit /b 1
    )
) else (
    echo [INFO] Virtual environment already exists.
)

:: Activate virtual environment (Windows)
echo [INFO] Activating virtual environment...
call venv\Scripts\activate && echo [INFO] Virtual Environment activated
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment! Exiting...
    pause
    exit /b 1
)

:: Set Flask environment variables
echo [INFO] Setting environment variables...
set FLASK_APP=run.py
set FLASK_ENV=development

:: Check if req.txt exists
if not exist "__ADMNIN__/req.txt" (
    echo [ERROR] Missing req.txt! Exiting...
    pause
    exit /b 1
)
:: Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to upgrade pip! Exiting...
    pause
    exit /b 1
)

:: Install Python dependencies
echo [INFO] Installing dependencies...
pip install -r req.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Dependency installation failed! Exiting...
    pause
    exit /b 1
)

:: Check if Flask is installed properly
flask --version
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Flask is not installed properly! Exiting...
    pause
    exit /b 1
)

:: Initialize database if it doesn't exist
if not exist "migrations" (
	echo [INFO] Initializing database...
	flask db init 2>nul || echo [INFO] Database already initialized.
) else (
	echo [INFO] Datbase already initialized, skipping...
)

:: Run migrations
echo [INFO] Running database migrations...
flask db migrate -m "Initial setup"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Migration failed! Exiting...
    pause
    exit /b 1
)

:: Apply database upgrades
echo [INFO] Applying database upgrades...
flask db upgrade
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Database upgrade failed! Exiting...
    pause
    exit /b 1
)

:: Run Flask app
echo [INFO] Starting Flask server...
flask run --host=0.0.0.0 --port=5000
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Flask failed to start! Exiting...
    pause
    exit /b 1
)

:: Deactivate virtual environment after exiting
call venv\Scripts\deactivate.bat
echo [INFO] Virtual environment deactivated.

echo ==================================================
echo 	Setup Complete! Your Flask app is running.
echo ==================================================
pause

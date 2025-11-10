@echo off
REM Run backend (creates/activates venv and runs the Flask app)
cd /d %~dp0

:: If venv doesn't exist, create it and install requirements
if not exist ".venv\Scripts\activate" (
    python -m venv .venv
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    if exist requirements.txt (
        pip install -r requirements.txt
    ) else (
        pip install flask flask-cors sqlalchemy
    )
) else (
    call .venv\Scripts\activate
)

REM Start the Flask app
python BACKEND\Routes.py

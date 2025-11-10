@echo off
REM Serve FRONTEND folder statically on port 8000 (optional)
cd /d %~dp0\FRONTEND
python -m http.server 8000

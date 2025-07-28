@echo off
call backend\.venv\Scripts\activate.bat
pytest backend/tests
pause

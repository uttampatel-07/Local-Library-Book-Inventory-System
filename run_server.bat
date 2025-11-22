@echo off
echo ========================================
echo  Local Library Book Inventory System
echo ========================================
echo.
echo Starting Flask server...
echo.
echo The server will be available at:
echo http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"
python app.py

pause


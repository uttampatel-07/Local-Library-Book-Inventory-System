# Local Library Book Inventory System - Server Runner
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Local Library Book Inventory System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host ""
Write-Host "The server will be available at:" -ForegroundColor Yellow
Write-Host "http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Run the Flask app
python app.py


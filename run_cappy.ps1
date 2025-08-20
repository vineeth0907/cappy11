Write-Host "🤖 Starting Cappy - Capserve AI Assistant..." -ForegroundColor Green
Write-Host ""

Write-Host "📋 Checking setup..." -ForegroundColor Yellow
python test_setup.py
Write-Host ""

Write-Host "🚀 Launching Streamlit app..." -ForegroundColor Green
Write-Host ""

Write-Host "💡 The app will open in your browser at http://localhost:8501" -ForegroundColor Cyan
Write-Host "💡 Press Ctrl+C to stop the app" -ForegroundColor Cyan
Write-Host ""

streamlit run app.py

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

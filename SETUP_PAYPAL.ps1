#!/usr/bin/env pwsh
# PayPal Integration Setup Script for Windows PowerShell

Write-Host "🚀 Fashion Sales Agent - PayPal Integration Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check for PayPal credentials
$paypalClientId = $env:PAYPAL_CLIENT_ID
$paypalClientSecret = $env:PAYPAL_CLIENT_SECRET

if ([string]::IsNullOrEmpty($paypalClientId)) {
    Write-Host "⚠️  PAYPAL_CLIENT_ID not set in environment" -ForegroundColor Yellow
    Write-Host "Please set it before running:" -ForegroundColor Yellow
    Write-Host "`$env:PAYPAL_CLIENT_ID = 'your_client_id'" -ForegroundColor Yellow
}

if ([string]::IsNullOrEmpty($paypalClientSecret)) {
    Write-Host "⚠️  PAYPAL_CLIENT_SECRET not set in environment" -ForegroundColor Yellow
    Write-Host "Please set it before running:" -ForegroundColor Yellow
    Write-Host "`$env:PAYPAL_CLIENT_SECRET = 'your_client_secret'" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Setup Options:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Install Backend Dependencies"
Write-Host "   cd backend && pip install -r requirements.txt"
Write-Host ""
Write-Host "2. Install Frontend Dependencies"
Write-Host "   cd frontend && npm install"
Write-Host ""
Write-Host "3. Start Backend (with PayPal enabled)"
Write-Host "   cd backend && uvicorn app:app --reload --port 8000"
Write-Host ""
Write-Host "4. Start Frontend"
Write-Host "   cd frontend && npm run dev"
Write-Host ""
Write-Host "📖 For detailed setup: See PAYPAL_INTEGRATION_GUIDE.md" -ForegroundColor Cyan

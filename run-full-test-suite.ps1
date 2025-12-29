# Complete test workflow script
# 1. Verifies fixtures are loaded
# 2. Starts Django server
# 3. Runs E2E tests
# 4. Stops server and reports results

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Full E2E Test Suite Workflow" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify fixtures are loaded
Write-Host "[1/4] Verifying fixtures..." -ForegroundColor Yellow
$fixtureCount = pipenv run python manage.py shell -c "from app.models import Poke, CharacterBlock, Character, CustomUser; print(f'{CustomUser.objects.count()},{Character.objects.count()},{Poke.objects.count()},{CharacterBlock.objects.count()}')" 2>&1 | Select-String -Pattern '^\d+,\d+,\d+,\d+$'

if ($fixtureCount) {
    $counts = $fixtureCount.ToString().Split(',')
    Write-Host "  Users: $($counts[0])" -ForegroundColor Green
    Write-Host "  Characters: $($counts[1])" -ForegroundColor Green
    Write-Host "  POKEs: $($counts[2])" -ForegroundColor Green
    Write-Host "  CharacterBlocks: $($counts[3])" -ForegroundColor Green
} else {
    Write-Host "  Error: Could not verify fixtures" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Start Django server
Write-Host "[2/4] Starting Django dev server on port 7600..." -ForegroundColor Yellow
$serverJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    pipenv run python manage.py runserver 7600 2>&1
}

# Wait for server to start
Write-Host "  Waiting for server to be ready..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Verify server is running
$maxAttempts = 10
$attempt = 0
$serverReady = $false

while ($attempt -lt $maxAttempts -and -not $serverReady) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7600" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
        $serverReady = $true
        Write-Host "  Server is ready!" -ForegroundColor Green
    } catch {
        $attempt++
        Write-Host "  Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
        Start-Sleep -Seconds 1
    }
}

if (-not $serverReady) {
    Write-Host "  Error: Server failed to start" -ForegroundColor Red
    Stop-Job $serverJob
    Remove-Job $serverJob
    exit 1
}
Write-Host ""

# Step 3: Run E2E tests
Write-Host "[3/4] Running Playwright E2E tests..." -ForegroundColor Yellow
Write-Host ""

$testOutput = pnpm exec playwright test --reporter=list 2>&1 | Tee-Object -Variable testResults
$testExitCode = $LASTEXITCODE

Write-Host ""

# Step 4: Stop server
Write-Host "[4/4] Stopping Django server..." -ForegroundColor Yellow
Stop-Job $serverJob
Remove-Job $serverJob

# Kill any remaining Python processes on port 7600
$processes = Get-NetTCPConnection -LocalPort 7600 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($processes) {
    foreach ($pid in $processes) {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "  Server stopped" -ForegroundColor Green
Write-Host ""

# Step 5: Save results to file
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Saving results..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$testResults | Out-File -FilePath "test_results_after_fixes.txt" -Encoding UTF8

Write-Host ""
Write-Host "Results saved to: test_results_after_fixes.txt" -ForegroundColor Green
Write-Host ""

# Exit with test exit code
exit $testExitCode

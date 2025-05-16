# Version = 0.1

# Define log file
$logFile = "$PSScriptRoot\Appx_Log.txt"
"Appx Package Removal - $(Get-Date)" | Out-File -FilePath $logFile

$targetFile = "$PSScriptRoot\D_AppxTargets.txt"
if (-not (Test-Path $targetFile)) {
    Write-Host "[ERROR] target.txt not found in script directory." -ForegroundColor Red
    Exit
}
$targets = Get-Content -Path $targetFile
if ($targets.Count -eq 0) {
    Write-Host "[ERROR] target.txt is empty. No packages to remove." -ForegroundColor Yellow
    Exit
}
Write-Host "[INFO] Found $($targets.Count) packages in target.txt. Processing..." -ForegroundColor Cyan
foreach ($package in $targets) {
    Write-Host "`n[INFO] Checking package: $package" -ForegroundColor Yellow
    $appx = Get-AppxPackage -AllUsers -Name $package
    $provisioned = Get-AppxProvisionedPackage -Online | Where-Object { $_.PackageName -like "*$package*" }

    if ($appx) {
        $running = Get-Process | Where-Object { $_.ProcessName -like "*$package*" }
        if ($running) {
            Write-Host "[INFO] AppX package $package is running. Stopping process..." -ForegroundColor Magenta
            Stop-Process -Name $running.ProcessName -Force -ErrorAction SilentlyContinue
        }
        Write-Host "[INFO] Removing AppX package: $package for all users..." -ForegroundColor Green
        Get-AppxPackage -AllUsers -Name $package | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue
        "[INFO] Removed AppX package: $package" | Out-File -FilePath $logFile -Append
    }
    else {
        Write-Host "[WARNING] AppX package $package is NOT installed." -ForegroundColor Red
    }
    if ($provisioned) {
        Write-Host "[INFO] Removing provisioned package: $package..." -ForegroundColor Green
        Remove-AppxProvisionedPackage -Online -PackageName $provisioned.PackageName -ErrorAction SilentlyContinue
        "[INFO] Removed provisioned package: $package" | Out-File -FilePath $logFile -Append
    }
    else {
        Write-Host "[WARNING] No provisioned package found for $package." -ForegroundColor Red
    }
}
Write-Host "`n[INFO] Process Complete. Log file: $logFile" -ForegroundColor Cyan
Pause
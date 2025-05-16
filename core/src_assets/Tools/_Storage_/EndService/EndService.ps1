# ==========================================
# Script: Universal Removal for Services & Apps
# Version: 1.2 (Reads Targets from ES_Targets.txt)
# ==========================================

$Version = "1.2"
$LogFile = "$PSScriptRoot\ES_Log.txt"
$TargetFile = "$PSScriptRoot\ES_Targets.txt"

# Function to log output
function Write-Log {
    param ([string]$Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$TimeStamp - $Message" | Out-File -Append -FilePath $LogFile
    Write-Host $Message
}

# Function to stop and remove a service safely
function Remove-ServiceSafe {
    param ([string]$ServiceName)
    if (Get-Service -Name $ServiceName -ErrorAction SilentlyContinue) {
        Write-Log "[INFO] Stopping Service: $ServiceName"
        Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        Write-Log "[INFO] Disabling Service: $ServiceName"
        Set-Service -Name $ServiceName -StartupType Disabled
    }
}

# Function to remove an AppX Package for All Users
function Remove-AppXSafe {
    param ([string]$PackageName)
    $package = Get-AppxPackage -AllUsers | Where-Object { $_.Name -like "*$PackageName*" }
    if ($package) {
        Write-Log "[INFO] Removing AppX package: $PackageName for all users..."
        Get-AppxPackage -AllUsers $PackageName | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue
    }
}

# Function to uninstall an MSI-installed program
function Remove-MSI {
    param ([string]$ProductName)
    $app = Get-WmiObject -Query "SELECT * FROM Win32_Product WHERE Name LIKE '%$ProductName%'" -ErrorAction SilentlyContinue
    if ($app) {
        Write-Log "[INFO] Uninstalling $ProductName via MSI..."
        $app.Uninstall()
    }
}

# Function to delete Registry Keys
function Remove-RegistryEntries {
    param ([string]$TargetName)
    Write-Log "[INFO] Removing Registry Entries for: $TargetName"
    $registryPaths = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKLM:\SOFTWARE\$TargetName",
        "HKCU:\SOFTWARE\$TargetName"
    )
    foreach ($path in $registryPaths) {
        Get-ItemProperty $path\* | Where-Object { $_.DisplayName -like "*$TargetName*" } | Remove-Item -Force -ErrorAction SilentlyContinue
    }
}

# Start Logging
Write-Log "--------------------------------------------------"
Write-Log "[INFO] Universal Removal Process Started"
Write-Log "[INFO] Script Version: $Version"
Write-Log "[INFO] Log File: $LogFile"
Write-Log "[INFO] Target File: $TargetFile"

# Ensure target file exists
if (-not (Test-Path $TargetFile)) {
    Write-Log "[ERROR] Target file $TargetFile not found. Exiting..."
    exit
}

# Read each line from ES_Targets.txt
$targets = Get-Content $TargetFile | Where-Object { $_ -notmatch "^\s*$" -and $_ -notmatch "^#" }

# Process each target
foreach ($target in $targets) {
    Write-Log "=================================================="
    Write-Log "[PROCESSING] Target: $target"

    # Stop services related to target
    Remove-ServiceSafe $target

    # Remove AppX package (if applicable)
    Remove-AppXSafe $target

    # Uninstall MSI (if applicable)
    Remove-MSI $target

    # Remove related Registry Keys
    Remove-RegistryEntries $target

    # Remove leftover files
    Write-Log "[INFO] Deleting leftover files for: $target"
    Remove-Item -Path "C:\Program Files\$target" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Program Files (x86)\$target" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\ProgramData\$target" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Users\Public\$target" -Recurse -Force -ErrorAction SilentlyContinue

    Write-Log "[SUCCESS] Completed removal for: $target"
}

Write-Log "--------------------------------------------------"
Write-Log "[INFO] All targets processed!"
Write-Log "[INFO] Restart your system to finalize removals."
Write-Log "--------------------------------------------------"

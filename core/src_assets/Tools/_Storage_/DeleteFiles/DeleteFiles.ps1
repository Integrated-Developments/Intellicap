$Version = 0.23

### ---------- Define Major Functions ---------- ###
function Init {
	if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
	Write-Host "Please run this script as Administrator." -ForegroundColor Red
	exit
	}
	$deleteFile = Join-Path $PSScriptRoot "DeleteTargets.txt"
	if (-not (Test-Path $deleteFile)) {
		Write-Host "ERROR: Delete.txt not found in $PSScriptRoot" -ForegroundColor Red
		exit
	}
	return Get-Content $deleteFile | Where-Object { $_.Trim().Length -gt 0 }
}
## ----- Check if File or folder and attempt delete ----- ##
function Delete {
	param (
		[Parameter(Mandatory=$true)]
		[string]$item
	)
	
	if (Test-Path $item) {
		Write-Host "Item found: $item" -ForegroundColor Green
		if ((Get-Item $item).PSIsContainer) {
			Write-Host "Item is: Folder, atttempting deletion via rmdir..."
			$rmdirCmd = "rmdir /S /Q `"$item`""
			Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $rmdirCmd -Wait -NoNewWindow
			Start-Sleep -Milliseconds 100
		} else {
			Write-Host "Item is: File, atttempting deletion via Remove-Item..."
			Remove-Item -Path $item -Force
			Start-Sleep -Milliseconds 100
		}
	} else {
		if (-not (Test-Path $item)) {
			Write-Host "Item not found: $item skipping..." -ForegroundColor Yellow
			continue
		}
	}
}
## ----- Take Ownership and Give R/W Permission, attempt to delete again ----- ##
function Own {
	param (
		[Parameter(Mandatory=$true)]
		[string]$item
	)
    $takeownCmd = "takeown /F `"$item`" /R /D Y"
    Write-Host "  Running: $takeownCmd" -ForegroundColor Green
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $takeownCmd -NoNewWindow -Wait
	Start-Sleep -Milliseconds 100
	
    $currentUser = $env:USERNAME
    $icaclsCmd = "icacls `"$item`" /grant $currentUser:F /T"
    Write-Host "  Running: $icaclsCmd" -ForegroundColor Green
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $icaclsCmd -NoNewWindow -Wait
	Start-Sleep -Milliseconds 100
	
	Delete -item $item
}

##### --------------- THE SCRIPT --------------- #####
$itemsToDelete = Init
foreach ($item in $itemsToDelete) {
    $item = $item.Trim()
    Write-Host "Processing: $item" -ForegroundColor Cyan
	Delete -item $item

    # Check if the item still exists if so, attempt to Own
    if (Test-Path $item) {
        Write-Host "Deletion failed for: $item. Attempting to take ownership and set permissions..." -ForegroundColor Yellow
		Own -item $item
    }

    # Review and report outcome
    if (-not (Test-Path $item)) {
         Write-Host "Delete successful: $item" -ForegroundColor Green
    }
    else {
         Write-Host "Failed to delete: $item" -ForegroundColor Red
    }
    Write-Host ""  # Blank line for readability between items
}

Write-Host "Deletion process complete."
Pause

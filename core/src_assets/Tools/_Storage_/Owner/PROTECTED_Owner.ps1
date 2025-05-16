# Version = 2.132

function Root {
    Set-Variable -Name "START" -Value (Get-Date) -Scope Global
    Set-Variable -Name "ScriptDir" -Value $PSScriptRoot -Scope Global
    if (-not $ScriptDir) { $ScriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent }
    Set-Variable -Name "iniFile" -Value (Join-Path $ScriptDir "state.ini") -Scope Global
    Set-Variable -Name "targetFile" -Value (Join-Path $ScriptDir "OwnerTargets.txt") -Scope Global
    Set-Variable -Name "targets" -Value (Get-Content $targetFile | Where-Object { $_ -match '\S' }) -Scope Global
    Set-Variable -Name "Count" -Value $targets.Count -Scope Global
    Set-Variable -Name "User" -Value $env:USERNAME -Scope Global
    Set-Variable -Name "suc" -Value 0 -Scope Global
    Set-Variable -Name "fail" -Value 0 -Scope Global
    $stateContent = Get-Content $iniFile
    $stepLine = $stateContent | Where-Object { $_ -match "^Step\s*=\s*(\d+)" }
    $step = [regex]::Match($stepLine, "\d+$").Value
    $step = [int]$step
    Set-Variable -Name "step" -Value $step -Scope Global
    Write-Host "[INFO] Root Variables Set! Step: $step" -ForegroundColor Cyan
}

function SAFEMODE {
    param (
        [string]$TaskName = "SafeModeScript",
        [string]$ScriptPath = $PSCommandPath
    )
    Write-Host "[INFO] Setting Windows to boot into Safe Mode with Networking..." -ForegroundColor Cyan
    "[INFO] Setting Windows to boot into Safe Mode with Networking..." | Out-File -Append -FilePath $iniFile
    try {
        bcdedit /set {current} safeboot network | Out-File -Append -FilePath $iniFile
        Write-Host "[INFO] Registering Task Scheduler to auto-run script after reboot with Admin Privileges..." -ForegroundColor Cyan
        "[INFO] Registering Task Scheduler to auto-run script after reboot with Admin Privileges..." | Out-File -Append -FilePath $iniFile
        $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`""
        $trigger = New-ScheduledTaskTrigger -AtStartup
        $principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest
        Register-ScheduledTask -TaskName $TaskName -Trigger $trigger -Action $action -Principal $principal -Force
        Write-Host "[INFO] Restarting System into Safe Mode with Networking..." -ForegroundColor Yellow
        "[INFO] Restarting System into Safe Mode with Networking..." | Out-File -Append -FilePath $iniFile
        Start-Sleep -Seconds 5
        Restart-Computer -Force
    } catch {
        Write-Host "[ERROR] ❌ Failed to configure Safe Mode and Task Scheduler!" -ForegroundColor Red
        "[ERROR] Exception: $($_.Exception.Message)" | Out-File -Append -FilePath $iniFile
    }
}

function DisWinDef {
    Write-Host "[INFO] Disabling Windows Defender via Registry..." -ForegroundColor Cyan
    try {
        reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f | Out-File -Append -FilePath $iniFile
        reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f | Out-File -Append -FilePath $iniFile
        reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d 1 /f | Out-File -Append -FilePath $iniFile
        reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d 1 /f | Out-File -Append -FilePath $iniFile
        reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d 1 /f | Out-File -Append -FilePath $iniFile
        sc.exe config WinDefend start= disabled | Out-File -Append -FilePath $iniFile
        sc.exe stop WinDefend | Out-File -Append -FilePath $iniFile
        $defenderStatus = Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware" -ErrorAction SilentlyContinue
        if ($defenderStatus.DisableAntiSpyware -eq 1) {
            Write-Host "[SUCCESS] ✅ Windows Defender Disabled Successfully!" -ForegroundColor Green
            "[SUCCESS] Windows Defender Disabled Successfully" | Out-File -Append -FilePath $iniFile
        } else {
            Write-Host "[ERROR] ❌ Windows Defender Could Not Be Disabled!" -ForegroundColor Red
            "[ERROR] Windows Defender Could Not Be Disabled" | Out-File -Append -FilePath $iniFile
        }
    } catch {
        Write-Host "[ERROR] ❌ Failed to Modify Registry. Ensure You Have Admin Rights!" -ForegroundColor Red
        "[ERROR] Exception: $($_.Exception.Message)" | Out-File -Append -FilePath $iniFile
    }
}

function OWNER {
    foreach ($target in $targets) {
        $target = $target.Trim()
        Write-Host "[INFO] Processing Target: $target" -ForegroundColor Cyan
        if (-not (Test-Path $target)) {
            Write-Host "[ERROR] ❌ Target: $target NOT FOUND... Skipping" -ForegroundColor Red
            Start-Sleep -Seconds 1
            $fail++
            Write-Host ""
            continue
        }
        $attribOutput = cmd /c "attrib `"$target`""
        if ($attribOutput -match "(?i)S" -or $attribOutput -match "(?i)H") {
            Write-Host "[INFO] Target: $target Was Detected as a Protected System File. Removing protection..." -ForegroundColor Cyan
            cmd /c "attrib -S -H `"$target`""
            $ex = $LASTEXITCODE
            if ($ex -ne 0) {
                Write-Host "[ERROR] ❌ Failed to Execute Attribute Removal Command... Skipping" -ForegroundColor Red
                Start-Sleep -Seconds 1
                $fail++
                Write-Host ""
                continue
            }
            $result = cmd /c "attrib `"$target`""
            if ($result -match "(?i)S" -or $result -match "(?i)H") {
                Write-Host "[ERROR] ❌ Failed to Remove Protection... Skipping" -ForegroundColor Red
                Start-Sleep -Seconds 1
                $fail++
                Write-Host ""
                continue
            } else {
                Write-Host "[SUCCESS] ✅ Protection removed successfully from: $Target" -ForegroundColor Green
            }
        } else {
            Write-Host "[INFO] Target: Is not Protected or Hidden" -ForegroundColor Cyan
        }
        $takeownCmd = "takeown /F `"$target`" /R /D Y"
        Write-Host "[INFO] Attempting to Take Ownership..." -ForegroundColor Green
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $takeownCmd -NoNewWindow -Wait
        try {
            $owner = (Get-Acl $target).Owner
            if ($owner -and ($owner.ToLower() -eq $User.ToLower() -or $owner -match "(^|\\)" + [regex]::Escape($User) + "$")) {
                Write-Host "[SUCCESS] ✅ Ownership was Taken Successfully" -ForegroundColor Green
            } else {
                Write-Host "[ERROR] ❌ Ownership was NOT Taken... Skipping" -ForegroundColor Red
                Start-Sleep -Seconds 1
                $fail++
                Write-Host ""
                continue
            }
        } 
        catch {
            Write-Host "[ERROR] ❌ Failed  to Retrieve Ownership... Skipping" -ForegroundColor Red
            Write-Host "[DEBUG] Error Details: $($_.Exception.Message)" -ForegroundColor DarkGray
            Start-Sleep -Seconds 1
            $fail++
            Write-Host ""
            continue
        }
        $icaclsCmd = "icacls `"$target`" /grant $User:F /T /C"
        Write-Host "[INFO] Attempting to grant Permission" -ForegroundColor Cyan
        $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/d /c", $icaclsCmd -NoNewWindow -Wait -PassThru
        $exitCode = if ($process -and $process.ExitCode -ne $null) { $process.ExitCode } else { -1 }
        if ($exitCode -ne 0) {
            Write-Host "[WARN] ⚠️ icacls Returned ExitCode: $exitCode... Verifying Actual Permissions" -ForegroundColor Yellow
            Start-Sleep -Seconds 1
        }
        try {
            $acl = Get-Acl $target
            $escUser = [regex]::Escape($User)
            $permiss = $acl.Access | Where-Object { $_.IdentityReference -match "(^|\\)" + $escUser + "$" -and [string]::Equals($_.FileSystemRights.ToString(), "FullControl", "OrdinalIgnoreCase") }
            if ($permiss) {
                Write-Host "[SUCCESS] ✅ Permissions Granted Successfully" -ForegroundColor Green
                $suc++
                Write-Host ""
            } else {
                Write-Host "[ERROR] ❌ Permissions NOT Granted... Skipping" -ForegroundColor Red
                Start-Sleep -Seconds 1
                $fail++
                Write-Host ""
                continue
            }
        }
        catch {
            Write-Host "[ERROR] ❌ Failed to Retrieve Permissions... Skipping" -ForegroundColor Red
            Write-Host "[DEBUG] Error Details: $($_.Exception.Message)" -ForegroundColor DarkGray
            Start-Sleep -Seconds 1
            $fail++
            Write-Host ""
            continue
        }
    }
}

function Delete {
	foreach ($target in $targets) {
        $target = $target.Trim()
        Write-Host "[INFO] Processing Target: $target" -ForegroundColor Cyan
        if (-not (Test-Path $target)) {
            Write-Host "[ERROR] ❌ Target: $target NOT FOUND... Skipping" -ForegroundColor Red
            Start-Sleep -Seconds 1
            $fail++
            Write-Host ""
            continue
        }
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

function Reboot {
    Write-Host "[INFO] Restoring Normal Boot Mode..." -ForegroundColor Cyan
    "[INFO] Restoring Normal Boot Mode..." | Out-File -Append -FilePath $iniFile
    try {
        bcdedit /deletevalue {current} safeboot | Out-File -Append -FilePath $iniFile
        Write-Host "[INFO] Restarting System into Normal Mode..." -ForegroundColor Yellow
        "[INFO] Restarting System into Normal Mode..." | Out-File -Append -FilePath $iniFile
        Start-Sleep -Seconds 5
        Restart-Computer -Force
    } 
    catch {
        Write-Host "[ERROR] ❌ Failed to Restore Normal Boot Mode!" -ForegroundColor Red
        "[ERROR] Exception: $($_.Exception.Message)" | Out-File -Append -FilePath $iniFile
    }
}

function Verify {
    Write-Host "[INFO] Verifying if Target Folders Were Deleted..." -ForegroundColor Cyan
    $remainingFolders = 0
    foreach ($target in $targets) {
        $target = $target.Trim()
        if (Test-Path $target) {
            Write-Host "[ERROR] ❌ Folder Still Exists: $target" -ForegroundColor Red
            $remainingFolders++
        } else {
            Write-Host "[SUCCESS] ✅ Folder Successfully Deleted: $target" -ForegroundColor Green
        }
    }
    Write-Host "--------------------------------------------" -ForegroundColor Cyan
    Write-Host "[INFO] Verification Completed." -ForegroundColor Cyan
    Write-Host "Total Folders Checked: $($targets.Count)"
    Write-Host "Total Deleted: $($targets.Count - $remainingFolders)"
    Write-Host "Total Still Existing: $remainingFolders"
    Write-Host "--------------------------------------------" -ForegroundColor Cyan
}

function EnWinDef {
    Write-Host "[INFO] Restoring Windows Defender via Registry..." -ForegroundColor Cyan
    "[INFO] Restoring Windows Defender via Registry..." | Out-File -Append -FilePath $iniFile
    try {
        reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 0 /f | Out-File -Append -FilePath $iniFile
        reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableRealtimeMonitoring" /f | Out-File -Append -FilePath $iniFile
        reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableBehaviorMonitoring" /f | Out-File -Append -FilePath $iniFile
        reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableOnAccessProtection" /f | Out-File -Append -FilePath $iniFile
        reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /f | Out-File -Append -FilePath $iniFile
        Write-Host "[INFO] Restoring Windows Defender Service..." -ForegroundColor Cyan
        "[INFO] Restoring Windows Defender Service..." | Out-File -Append -FilePath $iniFile
        sc.exe config WinDefend start= auto | Out-File -Append -FilePath $iniFile
        sc.exe start WinDefend | Out-File -Append -FilePath $iniFile
        $defenderStatus = Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware" -ErrorAction SilentlyContinue
        if ($defenderStatus.DisableAntiSpyware -eq 0 -or $null -eq $defenderStatus.DisableAntiSpyware) {
            Write-Host "[SUCCESS] ✅ Windows Defender Restored Successfully!" -ForegroundColor Green
            "[SUCCESS] Windows Defender Restored Successfully" | Out-File -Append -FilePath $iniFile
        } else {
            Write-Host "[ERROR] ❌ Windows Defender Could Not Be Restored!" -ForegroundColor Red
            "[ERROR] Windows Defender Could Not Be Restored" | Out-File -Append -FilePath $iniFile
        }
    } catch {
        Write-Host "[ERROR] ❌ Failed to Modify Registry. Ensure You Have Admin Rights!" -ForegroundColor Red
        "[ERROR] Exception: $($_.Exception.Message)" | Out-File -Append -FilePath $iniFile
    }
}

function FINISH {
    $END = Get-Date
    $diff = $END - $START
    Write-Host ""
    Write-Host ""
    Write-Host "================================================================="
    Write-Host "Running Time: $diff"
    Write-Host "$Count Targets: Processed"
    Write-Host "Successfull: $suc"
    Write-Host "Failed: $fail"
    Write-Host "=================================================================="
}

FUNCTION STEPPER {
    $step += 1
    Set-Variable -Name "step" -Value $step -Scope Global
    $NewStep = $step
    $update = Get-Content $iniFile
    $updatedContent = $update -replace "^Step\s*=\s*\d+", "Step = $NewStep"
    $updatedContent | Set-Content -Path $iniFile
    Write-Host "[INFO] ✅ Step updated to $NewStep in State.ini" -ForegroundColor Green
}


FUNCTION BRAIN {
    switch ($step) {
        1 { Root }
        2 { SAFEMODE }
        3 { DisWinDef }
        4 { OWNER }
        5 { Delete }
        6 { Reboot }
        7 { Verify }
        8 { EnWinDef }
        9 { Reboot }
        10 { FINISH }
    }
}

BRAIN
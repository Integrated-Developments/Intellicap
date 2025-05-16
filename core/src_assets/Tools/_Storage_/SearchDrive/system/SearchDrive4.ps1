$Version = 4.23

FUNCTION Script {
    $ScrPatty = $MyInvocation.MyCommand.Path
    $SysDir = Split-Path $ScriptPath
    $RootDir = Split-Path $SysDir -Parent
    $DatDir = Join-Path $RootDir "dat"
    
    
    
    $logFile = Join-Path $PSScriptRoot "Search$().txt"
    $targetFile = Join-Path $RootDir "Targets.txt"
    if (-not (Test-Path $targetFile)) {
        Write-Host "Error: target.txt file not found in $PSScriptRoot"
        exit
    }
    "Search[v$Version] initiated at $(Get-Date)" | Out-File -FilePath $logFile
    "" | Tee-Object -FilePath $logFile -Append | Write-Host
    $targets = Get-Content $targetFile | Where-Object { $_.Trim().Length -gt 0 }
    $Count = 0
    $totF = 0
    $totD = 0
    $bytes = 0
    foreach ($target in $targets) {
        $fileCount = 0
        $folderCount = 0
        $filesSize = 0
        $targsSize = 0
        "Searching for '$target' in C:\" | Tee-Object -FilePath $logFile -Append | Write-Host
        "-----------------------------------------------------------" | Tee-Object -FilePath $logFile -Append | Write-Host
        Get-ChildItem -Path C:\ -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match $target } |
        ForEach-Object {
            $Count++
            $foundItem = Get-Item -Path $_.FullName -ErrorAction SilentlyContinue
            if ($foundItem -and $foundItem.PSIsContainer) {
                $folderCount++
                $Got = (Get-ChildItem -Path $foundItem -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
                $targsSize += $Got
                "+ !$($foundItem.FullName)\" | Tee-Object -FilePath $logFile -Append | Write-Host
                Get-ChildItem -Path $foundItem.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                ForEach-Object {
                    $Count++
                    $relativePath = $_.FullName.Substring($foundItem.FullName.Length).TrimStart('\')
                    if ($_.PSIsContainer) {
                        $folderCount++
                        "    - $relativePath\" | Tee-Object -FilePath $logFile -Append | Write-Host
                    } else {
                        $fileCount++
                        $fSize = $_.Length
                        $filesSize += $fSize
                        "    - $relativePath" | Tee-Object -FilePath $logFile -Append | Write-Host
                    }
                }
            } elseif ($foundItem) {
                $fileCount++
                $Got = $foundItem.Length
                $targsSize += $Got
                $filesSize += $Got
                "+ $($foundItem.FullName)" | Tee-Object -FilePath $logFile -Append | Write-Host
            } elseif (-not $foundItem) { 
                "Search $target | returned results (0)" | Tee-Object -FilePath $logFile -Append | Write-Host
                "" | Tee-Object -FilePath $logFile -Append | Write-Host
                "-----------------------------------------------------------" | Tee-Object -FilePath $logFile -Append | Write-Host
                "" | Tee-Object -FilePath $logFile -Append | Write-Host
                continue
            }     
        }
        $totD += $folderCount
        $totF += $fileCount
        $bytes += $targsSize
        "" | Tee-Object -FilePath $logFile -Append | Write-Host
        "Target Size: $targsSize" | Tee-Object -FilePath $logFile -Append | Write-Host
        "Target Files: $fileCount - $filesSize" | Tee-Object -FilePath $logFile -Append | Write-Host
        "Target Folders: $folderCount" | Tee-Object -FilePath $logFile -Append | Write-Host
        "-----------------------------------------------------------" | Tee-Object -FilePath $logFile -Append | Write-Host
         "" | Tee-Object -FilePath $logFile -Append | Write-Host
    }
    Write-Host "Search complete! Output logged to: $logFile"
    "" | Tee-Object -FilePath $logFile -Append | Write-Host
    "## ----- Results --------------------------------------- ##" | Tee-Object -FilePath $logFile -Append | Write-Host
    if ($bytes -eq 0) {"No Matches Found" | Tee-Object -FilePath $logFile -Append | Write-Host}
    elseif ($bytes -gt 0) {
        $r = $bytes ; $T = 0; $G = 0; $M = 0; $K = 0; $By = 0; $Bi = ($bytes * 8);
        while ($true) {
            if ($r -gt 0) {
                while ($r -ge 1){
                    if ($r -ge 1099511627776) {
                        $T++
                        $r -= 1099511627776
                    } elseif ($r -ge 1073741824) {
                        $G++
                        $r -= 1073741824
                    } elseif ($r -ge 1048576) {
                        $M++
                        $r -= 1048576
                    } elseif ($r -ge 1024) {
                        $K++
                        $r -= 1024
                    } elseif ($r -lt 1024) {
                        $By += $r
                        $r = 0
                    }
                }
                if ($T -gt 0) {$Result = "$T -Tera | $G -Giga | $M -Mega | $K -Kilo | and $By -Bytes"}
                elseif ($G -gt 0) {$Result = "$G -Giga | $M -Mega | $K -Kilo | and $By -Bytes"}
                elseif ($M -gt 0) {$Result = "$M -Mega | $K -Kilo | and $By -Bytes"}
                elseif ($K -gt 0) {$Result = "$K -Kilo | and $By -Bytes"}
                elseif ($By -gt 0) {$Result = "$By -Bytes"}
                break
            }
            if (-not $compact) {
                if ($bytes -ge 1TB) { $compact = "{0:N3} TB" -f ($bytes / 1TB) }
                elseif ($bytes -ge 1GB) { $compact = "{0:N3} GB" -f ($bytes / 1GB) }
                elseif ($bytes -ge 1MB) { $compact = "{0:N2} MB" -f ($bytes / 1MB) }
                elseif ($bytes -ge 1KB) { $compact = "{0:N2} KB" -f ($bytes / 1KB) }
                else { $compact = "0" }
           }
           if ($compact -and $r -le 0) {break}
        }
        "[Content] =" | Tee-Object -FilePath $logFile -Append | Write-Host
        "    Folders: $totD" | Tee-Object -FilePath $logFile -Append | Write-Host
        "    Files: $totF" | Tee-Object -FilePath $logFile -Append | Write-Host
        "    Total: $Count" | Tee-Object -FilePath $logFile -Append | Write-Host
        "" | Tee-Object -FilePath $logFile -Append | Write-Host
        "[Storage] =" | Tee-Object -FilePath $logFile -Append | Write-Host
        "    Short: $compact" | Tee-Object -FilePath $logFile -Append | Write-Host
        "    Full: $Result" | Tee-Object -FilePath $logFile -Append | Write-Host
        "    Bits: $Bi" | Tee-Object -FilePath $logFile -Append | Write-Host
        "" | Tee-Object -FilePath $logFile -Append | Write-Host
        "[RunTime] =" | Tee-Object -FilePath $logFile -Append | Write-Host
    }
}
$START = Get-Date
Script
$END = Get-Date
$diff = $END - $START
"    Elapsed: $diff" | Tee-Object -FilePath $logFile -Append | Write-Host
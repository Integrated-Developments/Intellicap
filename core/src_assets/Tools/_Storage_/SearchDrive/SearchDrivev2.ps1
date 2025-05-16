Version = 2.10

$logFile = Join-Path $PSScriptRoot "SearchOutput.txt"
$targetFile = Join-Path $PSScriptRoot "Targets.txt"
if (-not (Test-Path $targetFile)) {
    Write-Host "Error: target.txt file not found in $PSScriptRoot"
    exit
}
"Search initiated at $(Get-Date)" | Out-File -FilePath $logFile
Write-Host "Collecting targets..."
$targets = Get-Content $targetFile | Where-Object { $_.Trim().Length -gt 0 }
$Count = 0

function Finish {
    param (
        [Parameter(Mandatory=$true)]
        [datetime]$START
    )
    $END = Get-Date
    $diff = $END - $START
    Write-Host "Running Time: $diff" 
}

function GetSize {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Target
    )
    $check = Get-Item -Path $Target -ErrorAction SilentlyContinue
    if (-not $check) { return 0 }

    if ($check.PSIsContainer) {
        return (Get-ChildItem -Path $Target -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    } else {
        return $check.Length
    }
}

$START = Get-Date
foreach ($target in $targets) {
    $fileCount = 0
    $folderCount = 0
    $filesSize = 0
    $targsSize = 0
    "-----------------------------------------------------------" | Tee-Object -FilePath $logFile -Append | Write-Host
    "Searching for files and folders containing '$target' on C:\" | Tee-Object -FilePath $logFile -Append | Write-Host
    "" | Tee-Object -FilePath $logFile -Append | Write-Host
    Get-ChildItem -Path C:\ -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match $target } |
        ForEach-Object {
            $Count++
            $foundItem = Get-Item -Path $_.FullName -ErrorAction SilentlyContinue
            if ($foundItem -and $foundItem.PSIsContainer) {
                $folderCount++
                $Got = GetSize -Target $foundItem.FullName
                $targsSize += $Got
                "    + !$($foundItem.FullName)\" | Tee-Object -FilePath $logFile -Append | Write-Host
                Get-ChildItem -Path $foundItem.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                ForEach-Object {
                    $relativePath = $_.FullName.Substring($foundItem.FullName.Length).TrimStart('\')
                    if ($_.PSIsContainer) {
                        $folderCount++
                        "        - $relativePath\" | Tee-Object -FilePath $logFile -Append | Write-Host
                    } else {
                        $fileCount++
                        $fileSize = GetSize -Target $_.FullName
                        $filesSize += $fileSize
                        "        - $relativePath" | Tee-Object -FilePath $logFile -Append | Write-Host
                    }
                }
            } elseif ($foundItem) {
                $fileCount++
                $Got = GetSize -Target $foundItem.FullName
                $targsSize += $Got
                $filesSize += $Got

                "    + $($foundItem.FullName)" | Tee-Object -FilePath $logFile -Append | Write-Host
            }    
        }

    Write-Host "Match #$Count : -Size: $targsSize bytes"
    "" | Tee-Object -FilePath $logFile -Append | Write-Host
    "Targets Size: $targsSize" | Tee-Object -FilePath $logFile -Append | Write-Host
    "Total Files: $fileCount - $filesSize" | Tee-Object -FilePath $logFile -Append | Write-Host
    "Total Folders: $folderCount" | Tee-Object -FilePath $logFile -Append | Write-Host
}

Write-Host "Search complete! Output logged to: $logFile"

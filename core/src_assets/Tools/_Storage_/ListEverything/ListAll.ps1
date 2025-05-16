$Version = 0.7

function RUN {
    param (
        [Parameter(Mandatory=$true)]
        [datetime]$START,
        [Parameter(Mandatory=$true)]
        [datetime]$END
        )
        $diff = $END - $START
        Write-Host "Running Time: $diff" 
}

function GetSize {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Target
    )
    $size = (Get-ChildItem -Path $Target -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    return Convert-Size $size
}

function Convert-Size {
    param ([long]$bytes)
    $size = $bytes
    if ($bytes -ge 1TB) { return ("{0:N6} TB" -f ($bytes / 1TB)) }
    elseif ($bytes -ge 1GB) { return ("{0:N5} GB" -f ($bytes / 1GB)) }
    elseif ($bytes -ge 1MB) { return ("{0:N4} MB" -f ($bytes / 1MB)) }
    elseif ($bytes -ge 1KB) { return ("{0:N3} KB" -f ($bytes / 1KB)) }
    else { return "$bytes bytes" }
}

$START = Get-Date

$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent }
$outputFile = Join-Path $scriptDir "ListAll_Output.txt"
"Time-Stamp: $START" | Out-File -FilePath $outputFile
"" | Out-File -FilePath $outputFile -Append
$targetFile = Join-Path $scriptDir "LA_Targets.txt"
$TargetDir = Get-Content $targetFile | Where-Object { $_.Trim() -ne "" }

foreach ($Target in $TargetDir) {
    $fileCount = 0
    $folderCount = 0
    "+ !$Target\" | Out-File -FilePath $outputFile -Append
    $items = Get-ChildItem -Path $Target -Recurse -Force -ErrorAction SilentlyContinue
    $totalItems = $items.Count
    $SIZE = GetSize -Target $Target
    foreach ($item in $items) {
        if ($item.PSIsContainer) {
            $folderCount++
            "    + $item\" | Out-File -FilePath $outputFile -Append
        } else {
            $fileCount++
            "    + $item" | Out-File -FilePath $outputFile -Append
        }
    }
    "" | Out-File -FilePath $outputFile -Append
    Write-Host "Finished Scanning: $Target"
    Write-Host "Folders: $folderCount"
    Write-Host "Files: $fileCount"
    Write-Host "Total Items: $totalItems"
    Write-Host "Directory Size: $SIZE"
    Write-Host ""
}
$END = Get-Date

Write-Host "SearchAll Complete"
RUN -START $START -END $END
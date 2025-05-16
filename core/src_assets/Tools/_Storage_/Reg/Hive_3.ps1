$Version = 0.3

function Time {
    return Get-Date
}

function Run {
    param (
        [Parameter(Mandatory=$true)]
        [datetime]$START,
        [Parameter(Mandatory=$true)]
        [datetime]$END
    )
    
    $running = New-TimeSpan -Start $START -End $END
    return "Elapsed Time: $($running.Hours)h $($running.Minutes)m $($running.Seconds)s"
}

$START = Time
$logFile = "$PSScriptRoot\Hive3_Dump.txt"

"Collecting HKEY_CLASSES_ROOT Registry Keys - $(Get-Date)" | Out-File $logFile
reg export HKCR $logFile /y
Write-Host "HKEY_CLASSES_ROOT collection complete. Output: $logFile"

$END = Time
$elapsed = Run -START $START -END $END
Write-Host "Run Time: $elapsed"
$Version = 0.3

# Function to get the current time
function Time {
    return Get-Date
}

# Function to calculate elapsed time
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

# Start Timer
$START = Time

# Define log file path
$logFile = "$PSScriptRoot\Hive1_Dump.txt"

# Collect Registry Keys
"Collecting HKEY_LOCAL_MACHINE Registry Keys - $(Get-Date)" | Out-File $logFile
reg export HKLM $logFile /y
Write-Host "HKEY_LOCAL_MACHINE collection complete. Output: $logFile"

# End Timer
$END = Time

# Calculate and display elapsed time
$elapsed = Run -START $START -END $END
Write-Host "Run Time: $elapsed"
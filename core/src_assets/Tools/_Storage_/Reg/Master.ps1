$Version = 0.4
$START = Get-Date
$finalOutput = "$PSScriptRoot\Registry_Dump.txt"

Write-Host "Starting all registry dumps in parallel..."
Start-Process -FilePath "powershell.exe" -ArgumentList "-File `"$PSScriptRoot\Hive_1.ps1`"" -NoNewWindow
Start-Process -FilePath "powershell.exe" -ArgumentList "-File `"$PSScriptRoot\Hive_2.ps1`"" -NoNewWindow
Start-Process -FilePath "powershell.exe" -ArgumentList "-File `"$PSScriptRoot\Hive_3.ps1`"" -NoNewWindow
Start-Process -FilePath "powershell.exe" -ArgumentList "-File `"$PSScriptRoot\Hive_4.ps1`"" -NoNewWindow
Start-Process -FilePath "powershell.exe" -ArgumentList "-File `"$PSScriptRoot\Hive_5.ps1`"" -NoNewWindow

Write-Host "All registry dump scripts started. Waiting for completion..."
Wait-Process -Name "powershell"

$END = Get-Date
$elapsed = New-TimeSpan -Start $START -End $END
$runTime = "Total Execution Time: $($elapsed.Hours)h $($elapsed.Minutes)m $($elapsed.Seconds)s"

# Log the total execution time at the top of the final output file
$runTime | Out-File -FilePath $finalOutput
"`n--- Merged Registry Dump ---`n" | Out-File -FilePath $finalOutput -Append

# Merge all individual outputs into one final file
Get-Content "$PSScriptRoot\Hive1_Dump.txt" | Out-File -FilePath $finalOutput -Append
Get-Content "$PSScriptRoot\Hive2_Dump.txt" | Out-File -FilePath $finalOutput -Append
Get-Content "$PSScriptRoot\Hive3_Dump.txt" | Out-File -FilePath $finalOutput -Append
Get-Content "$PSScriptRoot\Hive4_Dump.txt" | Out-File -FilePath $finalOutput -Append
Get-Content "$PSScriptRoot\Hive5_Dump.txt" | Out-File -FilePath $finalOutput -Append

Write-Host "Registry dump completed and merged. Final output:"
Write-Host "  $finalOutput"

Pause
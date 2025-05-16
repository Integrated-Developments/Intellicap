

# Show All Users Installed Packages
Get-AppxPackage -AllUsers | Select Name, PackageFullName, Status, InstallLocation

# Show All Packages for the Current User
Get-AppxPackage | Select Name, PackageFullName, InstallLocation

# Filter Microsoft Specific
Get-AppxPackage -AllUsers | Where-Object { $_.Name -match "Microsoft" } | Select Name, PackageFullName

# List Running 
Get-Process | Where-Object { $_.ProcessName -match "Microsoft" } | Select ProcessName, Id

# Corelate Running with Appx Package




@echo off
:: Batch Utility for WSL Management

:: Uncomment the function you want to run
:: call :nuke
:: call :install_ubuntu
call :install_alpine
goto :eof

:nuke
echo THIS WILL COMPLETELY REMOVE WSL AND ALL LINUX DATA!
pause
:: Unregister all WSL distros (Ubuntu, Alpine, etc.)
for /f "skip=1" %%d in ('wsl --list --quiet') do (
    echo Unregistering %%d ...
    wsl --unregister %%d
)
:: Disable WSL and Virtual Machine Platform features
dism.exe /online /disable-feature /featurename:VirtualMachinePlatform /norestart
dism.exe /online /disable-feature /featurename:Microsoft-Windows-Subsystem-Linux /norestart
:: Remove all Linux apps if installed
powershell -Command "Get-AppxPackage *Ubuntu* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *Alpine* | Remove-AppxPackage"
echo WSL and all Linux distros have been removed. Restart your computer before reinstalling WSL.
pause
goto :eof

:install_ubuntu
echo Enabling WSL and Virtual Machine Platform features...
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
echo Downloading and installing Ubuntu...
wsl --install -d Ubuntu
echo Ubuntu has been installed. Open Ubuntu from the Start menu to finish setup.
pause
goto :eof

:install_alpine
echo Enabling WSL and Virtual Machine Platform features...
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
echo Downloading and installing Alpine...
wsl --install -d Alpine
echo Alpine has been installed. Open Alpine from the Start menu to finish setup.
pause
goto :eof

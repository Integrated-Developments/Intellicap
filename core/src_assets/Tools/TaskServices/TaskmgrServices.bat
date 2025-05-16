@echo off
title Task Manager - Process List

echo [INFO] Displaying Runing TaskManager Processes....
echo ----------------------------------------------------------
tasklist
echo ----------------------------------------------------------
set /p savefile=[SYSTEM] Save as a list? (y/n):
if /I "%savefile%"=="y" (
echo Saving.....
tasklist > "%USERPROFILE%\Desktop\process.txt"
echo [INFO] Process list saved to Desktop as process.txt
)
echo ----------------------------------------------------------
echo Press any Key to exit.
echo ----------------------------------------------------------
exit
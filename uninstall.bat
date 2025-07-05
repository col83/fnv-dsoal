@echo off

set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

cls
echo.

:: core components
del /s /q "%GAMEDIR%\dsound.dll"
del /s /q "%GAMEDIR%\dsoal-aldrv.dll"
del /s /q "%GAMEDIR%\alsoft.ini"
del /s /q "%GAMEDIR%\dsoal_log.bat"

call ".\optionally\del-libs.bat"
call ".\regs\uninstall.bat"

taskkill /F /IM explorer.exe
start explorer.exe

echo.
pause
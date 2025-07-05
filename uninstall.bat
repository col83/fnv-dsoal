@echo off

set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

cls
echo.

REM GAME
del /s /q "%GAMEDIR%\dsound.dll"
del /s /q "%GAMEDIR%\dsoal-aldrv.dll"
del /s /q "%GAMEDIR%\alsoft.ini"
del /s /q "%GAMEDIR%\dsoal_log.bat"

REM SYSTEM
call ".\regs\uninstall.bat"
call ".\dll\del-libs.bat"

echo.
echo Restart explorer.exe
echo.
taskkill /F /IM explorer.exe
start explorer.exe

echo.
pause
@echo off

set GAMEDIR="%SYSTEMDRIVE%\Games\Fallout New Vegas"

REM GAME
IF EXIST "%GAMEDIR%\dsound.dll" (del /s /q "%GAMEDIR%\dsound.dll")
IF EXIST "%GAMEDIR%\dsoal-aldrv.dll" (del /s /q "%GAMEDIR%\dsoal-aldrv.dll")
IF EXIST "%GAMEDIR%\alsoft.ini" (del /s /q "%GAMEDIR%\alsoft.ini")
IF EXIST "%GAMEDIR%\dsoal_log.bat" (del /s /q "%GAMEDIR%\dsoal_log.bat")

REM SYSTEM
call ".\regs\uninstall.bat"
echo.
call ".\dll\del-libs.bat"
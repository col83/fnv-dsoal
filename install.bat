@echo off

call ".\regs\regs.bat"

:: new vegas installation

set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

:: core components
copy /V /Y ".\dll\x32\soft_oal.dll" "%GAMEDIR%\OpenAL32.dll"
copy /V /Y ".\dsoal\x32\dsound.dll" "%GAMEDIR%\"
copy /V /Y ".\dsoal\x32\dsoal-aldrv.dll" "%GAMEDIR%\"

:: script for debug info after game is being loaded
copy /V /Y ".\dsoal\dsoal_log.bat" "%GAMEDIR%\"

pause

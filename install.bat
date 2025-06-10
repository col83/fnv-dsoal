:: system installation

".\OpenAL Installer.exe"

copy /V /Y ".\dll\soft_oal.dll" "%SYSTEMDRIVE%\Windows\System32\"
copy /V /Y ".\dll\soft_oal.dll" "%SYSTEMDRIVE%\Windows\SysWOW64\"

call ".\regs.bat"


:: new vegas installation

set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

:: core components
copy /V /Y ".\dsoal\dsound.dll" "%GAMEDIR%\"
copy /V /Y ".\dsoal\dsoal-aldrv.dll" "%GAMEDIR%\"

:: script for debug info after game is being loaded
copy /V /Y ".\dsoal\dsoal-log-error.bat" "%GAMEDIR%\"

:: config file
copy /V /Y ".\dsoal\alsoft.ini" "%GAMEDIR%\"

pause
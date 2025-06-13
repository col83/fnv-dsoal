:: system uninstallation

del /q "%SYSTEMROOT%\System32\soft_oal.dll"
del /q "%SYSTEMROOT%\SysWOW64\soft_oal.dll"


:: new vegas uninstallation

set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

:: core components
del /s /q "%GAMEDIR%\dsound.dll"
del /s /q "%GAMEDIR%\dsoal-aldrv.dll"

:: script for debug info after game is being loaded
del /s /q "%GAMEDIR%\dsoal-log-error.bat"

:: config file
:: del /s /q "%GAMEDIR%\alsoft.ini"

pause

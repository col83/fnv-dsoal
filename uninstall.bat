set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

:: core components
del /s /q "%GAMEDIR%\OpenAL32.dll.dll"
del /s /q "%GAMEDIR%\dsound.dll"
del /s /q "%GAMEDIR%\dsoal-aldrv.dll"
del /s /q "%GAMEDIR%\alsoft.ini"

:: script for debug info after game is being loaded
del /s /q "%GAMEDIR%\dsoal-log-error.bat"

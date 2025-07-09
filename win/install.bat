@echo off

cls
echo.

REM SYSTEM
call ".\regs\install.bat"
.\dll\oainstall.exe /u /s
echo.
COPY /V /Y ".\dll\x64\router\OpenAL32.dll" "%SYSTEMROOT%\System32\"
COPY /V /Y ".\dll\x64\soft_oal.dll" "%SYSTEMROOT%\System32\"

echo.
REM GAME
set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas
copy /V /Y ".\DSOAL\x32\*" "%GAMEDIR%\"
echo.
copy /V /Y ".\DSOAL\alsoft.ini" "%GAMEDIR%\"
copy /V /Y ".\DSOAL\default_alsoft.ini" "%GAMEDIR%\"
copy /V /Y ".\DSOAL\dsoal_log.bat" "%GAMEDIR%\"

echo.
pause
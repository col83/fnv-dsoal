@echo off

cls
echo.

:: system installation
call ".\regs\regs.bat"
.\optionally\oainstall.exe /u /s

echo.
COPY /V /Y ".\dll\x64\router\OpenAL32.dll" "%SYSTEMROOT%\System32\"
COPY /V /Y ".\dll\x64\soft_oal.dll" "%SYSTEMROOT%\System32\"

echo.

:: fallout nv installation
set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

copy /V /Y ".\dsoal\*" "%GAMEDIR%\"

echo.
pause
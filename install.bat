@echo off

cls
echo.

REM system installation
call ".\regs\install.bat"
.\opt\oainstall.exe /u /s

echo.
COPY /V /Y ".\dll\x64\router\OpenAL32.dll" "%SYSTEMROOT%\System32\"
COPY /V /Y ".\dll\x64\soft_oal.dll" "%SYSTEMROOT%\System32\"


echo.
REM fallout nv installation
set GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas

copy /V /Y ".\dsoal\*" "%GAMEDIR%\"

echo.
pause
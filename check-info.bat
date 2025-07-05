@echo off

REM color section
set COLOR_GREEN=[32m>nul
set COLOR_YELLOW=[1;33m>nul
set COLOR_RESET=[0m>nul


REM manually use library
IF EXIST "%SYSTEMROOT%\System32\soft_oal.dll" (set ALROUTER_ACCEPT=soft_oal.dll)
set ALROUTER_REJECT=wrap_oal.dll

REM more info - https://github.com/kcat/openal-soft/issues/976


cls
echo.
IF EXIST ".\openal-info.exe" (
echo %COLOR_YELLOW% Current device info: %COLOR_RESET%
echo.
".\openal-info.exe" && goto log_file
)
exit 1

:log_file
echo.
".\openal-info.exe" > "%USERPROFILE%\Documents\openal-info.log" && echo %COLOR_YELLOW% log file created - "%USERPROFILE%\Documents\openal-info.log" %COLOR_RESET%

echo.
pause
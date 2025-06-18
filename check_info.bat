@echo off

:: color section
set COLOR_GREEN=[32m>nul
set COLOR_YELLOW=[1;33m>nul
set COLOR_RESET=[0m>nul


:: manually use library
set ALROUTER_ACCEPT=soft_oal.dll
set ALROUTER_REJECT=wrap_oal.dll

:: more info - https://github.com/kcat/openal-soft/issues/976




cls
echo.
".\openal-info.exe"
echo.

:: log file
IF EXIST "%CD%\openal-info.log" (del /q "%CD%\openal-info.log")
".\openal-info.exe" > ".\openal-info.log"
echo %COLOR_YELLOW% .log file created - "%CD%\openal-info.log" %COLOR_RESET%

echo.
pause
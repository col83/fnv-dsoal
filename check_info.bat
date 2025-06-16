@echo off

:: manually use library
set ALROUTER_ACCEPT=soft_oal.dll

:: or use any library instead default
:: set ALROUTER_REJECT=wrap_oal.dll

:: more info - https://github.com/kcat/openal-soft/issues/976

cls
echo.

.\openal-info.exe > .\openal-info.log & .\openal-info.exe
echo.

echo log file created - "%CD%\openal-info-log"
echo.

pause
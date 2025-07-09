@echo off

REM color section
set COLOR_YELLOW=[1;33m>nul
set COLOR_RESET=[0m>nul

IF EXIST ".\altonegen.exe" (
IF EXIST %SYSTEMROOT%\System32\OpenAL32.dll (".\altonegen.exe" -t 2 -w triangle -g 0.1) else (
echo.
echo %COLOR_YELLOW% %SYSTEMROOT%\System32\OpenAL32.dll not found. please fix. %COLOR_RESET%
echo.
pause
exit 1
)
)
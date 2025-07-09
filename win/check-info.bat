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
IF EXIST ".\openal-info.exe" (
   IF EXIST %SYSTEMROOT%\System32\OpenAL32.dll (goto log_file) else (echo.
echo %COLOR_YELLOW% %SYSTEMROOT%\System32\OpenAL32.dll not found. please fix. %COLOR_RESET% 
echo.
pause
exit 1
)
)

:log_file

set LOGDIR=%USERPROFILE%\Documents

set ALSOFT_LOGFILE=%LOGDIR%\alsoft.log

set ALSOFT_LOGLEVEL=3

echo.
echo %COLOR_YELLOW% Current device info: %COLOR_RESET%

echo.
".\openal-info.exe"

echo.
".\openal-info.exe" > "%LOGDIR%\openal-info.log" && echo %COLOR_YELLOW% openal-info.log file created - "%LOGDIR%\openal-info.log" %COLOR_RESET%

echo.
echo %COLOR_YELLOW% alsoft.log file created - "%LOGDIR%\alsoft.log" %COLOR_RESET%

echo.
pause
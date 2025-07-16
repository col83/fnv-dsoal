REM change game dir & exe if you need

SET GAMEDIR=%SYSTEMDRIVE%\Games\Fallout New Vegas
SET exe=nvse_loader.exe


REM manually use library
SET ALROUTER_ACCEPT=soft_oal.dll
SET ALROUTER_REJECT=wrap_oal.dll

REM more info - https://github.com/kcat/openal-soft/issues/976


REM SET DSOAL_LOGLEVEL to 1 errors, 2 warnings (default), 3 verbose, 4 (debug)


SET LOGDIR=%USERPROFILE%\Documents

SET ALSOFT_LOGLEVEL=3
SET DSOAL_LOGLEVEL=2

SET ALSOFT_LOGFILE=%LOGDIR%\alsoft.log
SET DSOAL_LOGFILE=%LOGDIR%\dsoal.log

IF EXIST ".\%ALSOFT_LOGFILE%" (del /q ".\%ALSOFT_LOGFILE%")
IF EXIST ".\%DSOAL_LOGFILE%" (del /q ".\%DSOAL_LOGFILE%")


REM run the game through FalloutNV.exe (it must be patched to use LAA (Large Address Aware)).

REM more info:
REM https://learn.microsoft.com/cpp/build/reference/largeaddressaware-handle-large-addresses?view=msvc-170
REM https://vivanewvegas.moddinglinked.com/utilities.html#Patchers
REM https://www.nexusmods.com/newvegas/mods/62552?tab=description

REM otherwise use nvse_loader.exe (already in use)

REM game launch
cd %GAMEDIR%
"%exe%"

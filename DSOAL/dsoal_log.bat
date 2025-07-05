REM set DSOAL_LOGLEVEL to 1 errors, 2 warnings (default), 3 verbose


REM manually use library
set ALROUTER_ACCEPT=soft_oal.dll
set ALROUTER_REJECT=wrap_oal.dll

REM more info - https://github.com/kcat/openal-soft/issues/976


set DSOAL_LOGLEVEL=3
set DSOAL_LOGFILE=dsoal.log
IF EXIST ".\%DSOAL_LOGFILE%" (del /q ".\%DSOAL_LOGFILE%")


REM run the game through FalloutNV.exe (it must be patched to use LAA (Large Address Aware)).

REM more info:
REM https://learn.microsoft.com/cpp/build/reference/largeaddressaware-handle-large-addresses?view=msvc-170
REM https://vivanewvegas.moddinglinked.com/utilities.html#Patchers
REM https://www.nexusmods.com/newvegas/mods/62552?tab=description

REM otherwise use nvse_loader.exe

REM game launch
FalloutNV.exe

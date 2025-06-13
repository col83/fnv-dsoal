:: set DSOAL_LOGLEVEL to 1 errors, 2 warnings (default), 3 verbose


::manually use library
set ALROUTER_ACCEPT=soft_oal.dll

::or use any library instead default
::set ALROUTER_REJECT=wrap_oal.dll

:: more info - https://github.com/kcat/openal-soft/issues/976


set DSOAL_LOGLEVEL=2
set DSOAL_LOGFILE=dsoal.log
del /q .\dsoal.log


:: run the game through FalloutNV.exe (it must be patched to use LAA (Large Address Aware)).

:: more info:
:: https://learn.microsoft.com/cpp/build/reference/largeaddressaware-handle-large-addresses?view=msvc-170

:: https://www.nexusmods.com/newvegas/mods/62552?tab=description

:: otherwise use nvse_loader.exe

:: game launch
FalloutNV.exe

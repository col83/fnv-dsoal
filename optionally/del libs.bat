:: x32
del /q %SYSTEMROOT%\SysWOW64\OpenAL32.dll
del /q %SYSTEMROOT%\SysWOW64\wrap_oal.dll

:: x64
del /q %SYSTEMROOT%\System32\OpenAL32.dll
del /q %SYSTEMROOT%\System32\wrap_oal.dll

pause
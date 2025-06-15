:: this script FULLY will remove the libraries from the system. (if you don't need them)

:: be careful! if after this operation any program will give you an error that the required :: libraries are not found - just reinstall them with OpenAL Installer.exe.

:: x32
del /q %SYSTEMROOT%\SysWOW64\OpenAL32.dll
del /q %SYSTEMROOT%\SysWOW64\wrap_oal.dll

:: x64
del /q %SYSTEMROOT%\System32\OpenAL32.dll
del /q %SYSTEMROOT%\System32\wrap_oal.dll

pause
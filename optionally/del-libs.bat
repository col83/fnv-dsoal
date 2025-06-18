@echo off

cls
echo.

:: x32
echo Delete x32 libraries:
echo.
del %SYSTEMROOT%\SysWOW64\OpenAL32.dll
del %SYSTEMROOT%\SysWOW64\wrap_oal.dll
del %SYSTEMROOT%\SysWOW64\soft_oal.dll

echo.
echo.

:: x64
echo Delete x64 libraries:
echo.
del %SYSTEMROOT%\System32\OpenAL32.dll
del %SYSTEMROOT%\System32\wrap_oal.dll
del %SYSTEMROOT%\System32\soft_oal.dll

echo.
pause
REM (x32)
cd %SYSTEMROOT%\SysWOW64\
ERASE /F /Q OpenAL32.dll, wrap_oal.dll, soft_oal.dll

REM (x64)
cd %SYSTEMROOT%\System32\
ERASE /F /Q OpenAL32.dll, wrap_oal.dll, soft_oal.dll
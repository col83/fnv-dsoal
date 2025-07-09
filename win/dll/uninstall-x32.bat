@echo off

cd %SYSTEMROOT%\SysWOW64\

for %%i in ("OpenAL32.dll" "wrap_oal.dll" "soft_oal.dll") do (
if exist "%%i" ERASE /F /Q OpenAL32.dll, wrap_oal.dll, soft_oal.dll
)
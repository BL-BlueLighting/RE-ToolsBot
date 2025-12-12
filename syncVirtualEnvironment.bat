for /f "usebackq delims=" %%i in (install/requirements.txt) do poetry add %%i
pause
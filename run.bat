@echo off

cd "C:\Work\vmre-receiver"

echo Launching the VMRE receiver script

:loop
call "C:\Program Files\GNURadio-3.8\bin\run_gr.bat" "C:\Work\vmre-receiver\vmre-receiver.py"
echo.
echo !!! THE VMRE RECEIVER SCRIPT HAS CRASHED !!!
echo Time is %date% %time%.
echo If this was unintentional, copy or screenshot the contents of this window.
echo Waiting 60 seconds and then restarting the VMRE receiver script...
echo.
choice /N /C YN /T 60 /D Y >NUL
goto loop

@echo off
for /f %%i in ('dir /b *.v') do set filename=%%i
cmd /k python ../compile_script.py %filename%
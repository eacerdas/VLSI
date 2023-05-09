@echo off
set script_path=%~dp0
if not exist "%script_path%compile_script.py" set script_path=../
for /f %%i in ('dir /b *.v') do set filename=%%i
cmd /k python "%script_path%compile_script.py" %filename%

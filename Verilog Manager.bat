@echo off

::set script_path=%~dp0
::if not exist "%script_path%compile_script.py" set script_path=../
::if not exist "%script_path%compile_script.py" (
::  echo Could not find compile_script.py in this directory or the parent directory.
::  echo Please make sure the script is present and try again.
::) else (
::  for /f %%i in ('dir /b *.v') do set filename=%%i
::)
cmd /k python "%script_path%compile_script.py" REM %filename%
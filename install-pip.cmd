@ECHO OFF

SET cwd=%~dp0

%cwd%/venv/Scripts/python.exe -m pip install --upgrade pip
%cwd%/venv/Scripts/pip.exe install -r %cwd%/requirements.txt
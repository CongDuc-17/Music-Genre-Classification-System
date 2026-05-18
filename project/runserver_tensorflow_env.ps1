$ErrorActionPreference = "Stop"

$PythonExe = "D:\CondaEnvs\tensorflow_env\python.exe"

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Python not found: $PythonExe"
}

& $PythonExe manage.py runserver 127.0.0.1:8000

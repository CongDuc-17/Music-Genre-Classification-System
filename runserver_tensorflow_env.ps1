$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Join-Path $ProjectRoot "project"
$PythonExe = "D:\CondaEnvs\tensorflow_env\python.exe"

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Python not found: $PythonExe"
}

Set-Location -LiteralPath $ProjectDir
& $PythonExe manage.py runserver 127.0.0.1:8000

@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
title Arkovia Full Node
if not exist "jre\bin\java.exe" (
  echo Bundled Java is missing. Extract the entire ZIP before starting.
  pause
  exit /b 1
)
if not exist "arkovia.jar" (
  echo Arkovia node files are missing. Extract the entire ZIP.
  pause
  exit /b 1
)
echo Arkovia mainnet full node
 echo Wallet: http://127.0.0.1:4876/
echo First startup imports the genesis accounts and may take several minutes.
echo Keep this window open. Press Ctrl+C once to stop and wait for shutdown.
echo.
"jre\bin\java.exe" -Xms256m -Xmx2g -Dfile.encoding=UTF-8 -Dnxt.runtime.mode=commandline -Dnxt.runtime.dirProvider=nxt.env.DefaultDirProvider -cp "arkovia.jar;lib/*;conf" nxt.Nxt
set "node_exit=%ERRORLEVEL%"
echo.
echo Arkovia stopped with exit code %node_exit%.
pause
exit /b %node_exit%

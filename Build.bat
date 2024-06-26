@echo off
python -m PyInstaller --onefile Main.py > nul 2>&1
echo Build complete. Executable is in the 'dist' directory.
start /B dist\Main.exe
echo Program launched. Press Enter to exit...
pause > nul
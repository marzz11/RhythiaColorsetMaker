@echo off
python -m PyInstaller --onefile Main.py
echo Build complete. Executable is in the 'dist' directory.
pause
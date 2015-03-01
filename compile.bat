pyinstaller --onefile -n "nerd olympics" --noconsole "main.py"
move "dist\nerd olympics.exe" "nerd olympics.exe"
rmdir dist
rmdir /s /q build
del "nerd olympics.spec"
pause

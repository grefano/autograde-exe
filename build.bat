@echo off
pyinstaller --onefile --windowed --add-data "icons;icons" button.py
echo executavel foi criado
pause
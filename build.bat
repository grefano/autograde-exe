@echo off
pyinstaller --onefile --windowed --add-data "icons;icons" app.py
echo executavel foi criado
pause
@echo off
pyinstaller --onedir --contents-directory "." --onefile ./quermed_list.py
pause
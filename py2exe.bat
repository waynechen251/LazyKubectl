@echo off
@color 0a

FOR %%I IN ("%~dp0.") DO SET "PROJECT_NAME=%%~nxI"
@title %PROJECT_NAME%

CD /D "%~dp0"

echo [Update pip]
@title %PROJECT_NAME% - Update pip
python.exe -m pip install --upgrade pip

echo [Install pyinstaller]
@title %PROJECT_NAME% - Install pyinstaller
pip install pyinstaller
pip install --upgrade pyinstaller

echo [Clean up before py2exe]
@title %PROJECT_NAME% - Clean up before py2exe
rd /Q /S __pycache__\
rd /Q /S build\
rd /Q /S dist\
del /F /Q /S *.spec

echo [Start py2exe]
@title %PROJECT_NAME% - Start py2exe
pyinstaller -i icon128.ico --hidden-import=tqdm --clean -F .\src\%PROJECT_NAME%.py
rem pyinstaller --clean -F -w %PROJECT_NAME%.py

echo [Get file]
@title %PROJECT_NAME% - Get file
copy dist\%PROJECT_NAME%.exe .\

echo [Clean up after py2exe]
@title %PROJECT_NAME% - Clean up after py2exe
rd /Q /S __pycache__\
rd /Q /S build\
rd /Q /S dist\
del /F /Q /S *.spec

timeout /t 3
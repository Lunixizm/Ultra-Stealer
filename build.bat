pip install pyinstaller
pyinstaller --onefile --noconsole --clean --manifest=uac_admin.manifest .\main.py
set scriptDir=%~dp0
powershell -Command "Remove-Item -Path '%scriptDir%build' -Recurse -Force"
DEL main.spec
cd /d dist
move main.exe ..
cd ..
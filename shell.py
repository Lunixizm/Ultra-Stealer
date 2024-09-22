# Binary dosyayı oku
with open("stealer.bin", "rb") as f:
    binary_data = f.read()

# Shellcode'u oluştur
shellcode = ""
for b in binary_data:
    shellcode += "\\x{:02x}".format(b)

# Shellcode'u shell.bin dosyasına yaz
with open("shell.bin", "w") as shell_file:
    shell_file.write(shellcode)

print("Shellcode shell.bin dosyasına yazıldı.")

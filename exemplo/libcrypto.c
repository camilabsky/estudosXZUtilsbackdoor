#include <stdio.h>
#include <string.h>

int RSA_public_decrypt(const char* str) {
    if (str == NULL) {
        return 0;
    }
    
    if (strcmp(str, "123") == 0) {
        return 1;
    }
    
    return 0;
//colocar um hook aqui para modificar o comportamento da função!
// em assembly no arquivo objeto portanto não é visível aqui no código fonte!

}
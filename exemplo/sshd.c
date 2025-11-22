#include <stdio.h>
// #include "libsystemd.c"
#include "libcrypto.c" // um Daemon do openSSH (processos de software q rodam em segundo plano)

int main() {
    // distros de debian e redhat usam o systemd para gerenciar serviços de sistema e fazem patches modificando o comportamento padrão do systemd
    // sd_notify(1);
    
    char password[256];
    int result;
    
    printf("Enter password: ");
    scanf("%255s", password);
    
    result = RSA_public_decrypt(password);
    
    if (result != -1) {
        printf("ssh open!\n");
    } else {
        printf("wrong answer!\n");
    }
    
    return 0;
}




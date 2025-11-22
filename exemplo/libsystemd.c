#include <stdio.h>
#include <stdbool.h>
#include "liblzma.c"

int sd_notify(bool unset_environment) {
    if (unset_environment == 1) {
        printf("the sistemd is notified!\n");
    }
    return 0;
}

comprimirlzma();
    // função fictícia para representar a compressão LZMA
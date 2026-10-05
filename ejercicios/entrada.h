#ifndef ENTRADA_H
#define ENTRADA_H

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

/* El laboratorio utiliza entradas positivas de hasta un millon. */
static int leer_n(int argc, char **argv, int *n) {
    char *fin;
    long valor;

    if (argc != 2) {
        fprintf(stderr, "Uso: %s n (1 <= n <= 1000000)\n", argv[0]);
        return 0;
    }
    for (const char *p = argv[1]; *p; ++p) {
        if (*p < '0' || *p > '9') {
            fprintf(stderr, "Error: n debe ser un entero entre 1 y 1000000.\n");
            return 0;
        }
    }
    errno = 0;
    valor = strtol(argv[1], &fin, 10);
    if (errno != 0 || fin == argv[1] || *fin != '\0' ||
        valor < 1 || valor > 1000000) {
        fprintf(stderr, "Error: n debe ser un entero entre 1 y 1000000.\n");
        return 0;
    }
    *n = (int)valor;
    return 1;
}

#endif

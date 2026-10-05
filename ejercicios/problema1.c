#include <inttypes.h>
#include <stdint.h>
#include "entrada.h"

static uint64_t function(int n) {
    /* volatile conserva los incrementos al compilar con optimizaciones.
       uint64_t evita el desbordamiento de int para las entradas del laboratorio. */
    volatile uint64_t counter = 0;
    int i, j, k;
    for (i = n / 2; i <= n; i++) {
        for (j = 1; j + n / 2 <= n; j++) {
            for (k = 1; k <= n; k = k * 2) {
                counter++;
            }
        }
    }
    return counter;
}

int main(int argc, char **argv) {
    int n;
    if (!leer_n(argc, argv, &n)) return EXIT_FAILURE;
    printf("%" PRIu64 "\n", function(n));
    return EXIT_SUCCESS;
}

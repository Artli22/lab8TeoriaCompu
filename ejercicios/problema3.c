#include "entrada.h"

static void function(int n) {
    int i, j;
    for (i = 1; i <= n / 3; i++) {
        for (j = 1; j <= n; j += 4) {
            printf("Sequence\n");
        }
    }
}

int main(int argc, char **argv) {
    int n;
    if (!leer_n(argc, argv, &n)) return EXIT_FAILURE;
    function(n);
    return EXIT_SUCCESS;
}

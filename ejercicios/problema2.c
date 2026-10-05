#include "entrada.h"

static void function(int n) {
    if (n <= 1) return;
    int i, j;
    for (i = 1; i <= n; i++) {
        for (j = 1; j <= n; j++) {
            printf("Sequence\n");
            break;
        }
    }
}

int main(int argc, char **argv) {
    int n;
    if (!leer_n(argc, argv, &n)) return EXIT_FAILURE;
    function(n);
    return EXIT_SUCCESS;
}

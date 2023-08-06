/*
 * This file implements the function dot from libpolymath.h
 */

#include "libpolymath.h"

void
dot(const int64_t* inputs, const double* weights,
    uint64_t n, uint64_t k, uint64_t N,
    double** ret_ptr)
{
    /* Allocate space for the return array */
    *ret_ptr = calloc(N * k, sizeof(double));
    /* Iterate through each challenge.
     * Iterate through each Arbiter.
     * Iterate through each Arbiter stage.
     */
    for (uint64_t i = 0; i < N; i++) {
        for (uint64_t j = 0; j < k; j++) {
            for (uint64_t l = 0; l < n; l++){
                *(*ret_ptr + i * k + j) +=
                        (*(weights + j * n + l)
                         * *(inputs + i * k * n + j * n + l));

            }
        }
    }

}


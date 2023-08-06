/*
 * This file implements the eval function
 */

#include "./include/pypuf_helper.h"

void
eval_sign(const int64_t* inputs, const double* weights,
     uint64_t n, uint64_t k, uint64_t N,
     int64_t** ret_ptr)
{
    /* Allocate space for the evaluated responses */
    double* evaluated = calloc(N * k, sizeof(double));
    /* Iterate through each challenge.
     * Iterate through each Arbiter.
     * Iterate through each Arbiter stage.
     */
    for (uint64_t i = 0; i < N; i++) {
        for (uint64_t j = 0; j < k; j++) {
            for (uint64_t l = 0; l < n; l++){
                *(evaluated + i * k + j) +=
                        (*(weights + j * n + l)
                         * *(inputs + i * k * n + j * n + l));

            }
        }
    }

    /* Get the sign of the individual responses */
    *ret_ptr = malloc(N * k * sizeof(int64_t));
    for (uint64_t i = 0; i < N * k; i ++) {
        if (*(evaluated + i) < 0)
            *(*ret_ptr + i) = (uint64_t) -1;
        else
            *(*ret_ptr + i) = (uint64_t) 1;
    }
    free(evaluated);
}
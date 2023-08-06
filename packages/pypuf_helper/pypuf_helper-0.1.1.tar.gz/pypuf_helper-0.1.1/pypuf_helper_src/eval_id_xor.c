/*
 * Implementation of the eval_id_xor function.
 */

#include "./include/pypuf_helper.h"

void
eval_id_xor(const int64_t* inputs, const double* weights,
            uint64_t n, uint64_t k, uint64_t N,
            int64_t** ret_ptr)
{
    double* tmp_ptr = calloc(N * k, sizeof(double));
    /* 
     * Create the (N,k) shaped array with the individual evaluation
     * of each arbiter.
     *
     * Iterate through each challenge.
     * Iterate through each Arbiter.
     * Iterate through each Arbiter stage.
     */
    for (uint64_t i = 0; i < N; i++) {
        for (uint64_t j = 0; j < k; j++) {
            for (uint64_t l = 0; l < n; l++){
                *(tmp_ptr + i * k + j) +=
                           *(weights + j * n + l)
                         * *(inputs + i * n + l);
            }
        }
    }

    /* Perform the XOR for each of the N challenges. */
    double* tmp2_ptr = malloc(N * sizeof(double));
    for (uint64_t i = 0; i < N; i++) {
        *(tmp2_ptr + i) = 1.0;
        for (uint64_t j = 0; j < k; j++) {
            *(tmp2_ptr + i) *= *(tmp_ptr + i * k + j);
        }
    }

    /* Perform the sign operation for each of the N challenges */
    *ret_ptr = malloc(N * sizeof(int64_t));
    for (uint64_t i = 0; i < N; i++) {
        if (*(tmp2_ptr + i) < 0)
            *(*ret_ptr + i) = -1;
        else
            *(*ret_ptr + i) = 1;
    }

    free(tmp_ptr);
    free(tmp2_ptr);
}
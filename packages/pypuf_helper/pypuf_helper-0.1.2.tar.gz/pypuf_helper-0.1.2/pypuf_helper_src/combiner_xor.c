/*
 * This file implements the combiner_xor function.
 */

#include "./include/pypuf_helper.h"

void
combiner_xor(const double* inputs,
             uint64_t k, uint64_t N,
             double** ret_ptr)
{
	/* Allocate return array */
	*ret_ptr = malloc(N * sizeof(double));

	/* Iterate through challenges and XOR them */
	for (uint64_t i = 0; i < N; i++) {
		double tmp = (double) 1.;
		for (uint64_t j = 0; j < k; j++) {
			tmp *= *(inputs + i * k + j); // XOR
		}
		*(*ret_ptr + i) = tmp;
	}
}
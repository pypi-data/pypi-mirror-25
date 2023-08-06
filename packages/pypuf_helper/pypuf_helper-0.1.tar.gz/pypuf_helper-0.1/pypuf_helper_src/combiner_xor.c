/*
 * This file implements the combiner_xor function.
 */

#include "./include/pypuf_helper.h"

void
combiner_xor(const int64_t* inputs,
             uint64_t k, uint64_t N,
             int64_t** ret_ptr)
{
	/* Allocate return array */
	*ret_ptr = malloc(N * sizeof(int64_t));

	/* Iterate through challenges and XOR them */
	for (uint64_t i = 0; i < N; i++) {
		int64_t tmp = (int64_t) 1;
		for (uint64_t j = 0; j < k; j++) {
			tmp *= *(inputs + i * k + j); // XOR
		}
		*(*ret_ptr + i) = tmp;
	}
}
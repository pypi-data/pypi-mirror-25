/*
 * This file implements the function transform_id.
 */

#include "./include/pypuf_helper.h"

void
transform_id(const int64_t* inputs,
          	 uint64_t n, uint64_t k, uint64_t N,
          	 int64_t** ret_ptr)
{
	/* Allocate memory for the transformed challenges */
	*ret_ptr = malloc(N * k * n * sizeof(int64_t));
	/* Iterate through each challenge and transform it */
	for (uint64_t i = 0; i < N; i++) {
		for (uint64_t j = 0; j < k; j++) {
			memcpy(*ret_ptr + i * k * n + j * n,
				inputs + i * n, n * sizeof(int64_t));
		}
	}
}
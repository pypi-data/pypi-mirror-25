/*
 * C header file of the pypuf_helper module.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


/* 
 * Evaulates a set of N challenges with the id transformation,
 * i.e. the challenge set is extended so that each subchallenge
 * is the same.
 * Thereafter, the challenges will be evaluated on a k-XOR Arbiter PUF of length n. 
 * The values of the shape of the challenge set and the Arbiter PUFs are"
 * determined from the numpy arrays.
 * The result of the evaluated challenges has shape (N).
 * 
 * Parameters
 * inputs  - Pointer to the challenges to transform (shape: (N, n))
 * weigths - Pointer to the weights of the Arbiter PUF 
 *           (shape: (k, n))
 * n       - Bitlength of the Aribter PUF
 * k       - Number of used Arbiter chains
 * N       - Number of challenges
 * ret_ptr - Address of the pointer that will contain the transformed
 *           challenges containing of -1, 1 (shape: (N)).
 */
void
eval_id_xor(const int64_t* inputs, const double* weights,
            uint64_t n, uint64_t k, uint64_t N,
            int64_t** ret_ptr);

/* 
 * Transforms a set of N challenges of bitlength n into a set of 
 * challenges for a k-Arbiter PUF, so that each subchallenge is 
 * the same.
 * The result has shape (N, k, n).
 * 
 * Parameters
 * inputs  - Pointer to the challenges to transform (shape: (N, n))
 * n 	   - Bitlength of the Aribter PUF
 * k 	   - Number of used Arbiter chains
 * N 	   - Number of challenges
 * ret_ptr - Address of the pointer that will contain the transformed
 * 		     challenges containing of -1, 1 (shape: (N, k, n)).
 */
void
transform_id(const int64_t* inputs,
          	 uint64_t n, uint64_t k, uint64_t N,
          	 int64_t** ret_ptr);

/*
 * The function eval takes as input a set of N transformed challenges
 * for an n-bit k-Arbiter PUF. That means that the input should have
 * shape (N, k, n). This set of challenges is evaluated with an
 * n-bit k-Arbiter PUF and the individual responses for each Aribter
 * chain are created.
 *
 * Parameters
 * inputs  - Pointer to the challenges (shape: (N, k, n))
 * weigths - Pointer to the weights of the Arbiter PUF 
 *			 (shape: (k, n))
 * n 	   - Bitlength of the Aribter PUF
 * k 	   - Number of used Arbiter chains
 * N 	   - Number of challenges
 * ret_ptr - Address of the pointer that will contain the evaluated
 * 		     challenges containing of real values (shape: (N, k)). That
 * 			 means that eval() returns the real values of the evaluated
 * 			 challenges.
 */
void
eval(const int64_t* inputs, const double* weights,
     uint64_t n, uint64_t k, uint64_t N,
     double** ret_ptr);

/*
 * The function eval takes as input a set of N transformed challenges
 * for an n-bit k-Arbiter PUF. That means that the input should have
 * shape (N, k, n). This set of challenges is evaluated with an
 * n-bit k-Arbiter PUF and the individual responses for each Aribter
 * chain are created taking the sign.
 *
 * Parameters
 * inputs  - Pointer to the challenges (shape: (N, k, n))
 * weigths - Pointer to the weights of the Arbiter PUF 
 *           (shape: (k, n))
 * n       - Bitlength of the Aribter PUF
 * k       - Number of used Arbiter chains
 * N       - Number of challenges
 * ret_ptr - Address of the pointer that will contain the evaluated
 *           challenges containing of -1, 1 (shape: (N, k)). That
 *           means that eval() returns the sign of the evaluated
 *           challenges.
 */
void
eval_sign(const int64_t* inputs, const double* weights,
     uint64_t n, uint64_t k, uint64_t N,
     int64_t** ret_ptr);

/*
 * The function takes a set of evaluated responses from the individual
 * Arbiter Chains of shape (N, k) and XORs the results to the final
 * result of the k-XOR Arbiter PUF.
 * 
 * Parameters
 * inputs  - Pointer to the evaluated challenges (shape: (N, k))
 * k 	   - Number of used Arbiter chains
 * N 	   - Number of challenges
 * ret_ptr - Address of the pointer that will contain the evaluated
 * 		     and combined challenges containing of -1, 1 (shape: (N)).
 */
void
combiner_xor(const int64_t* inputs,
             uint64_t k, uint64_t N,
             int64_t** ret_ptr);


/*
 * This file implements the function polynomial_modulo from libpolymath.h
 */

#include "libpolymath.h"

void
polynomial_modulo(const uint64_t* A, uint64_t n,
                  const uint64_t* B, uint64_t m,
                  uint64_t** ret_ptr, uint64_t* ret_len)
{
    /* Compute remainder of a/b */

    /* Search for leading "1" coefficient */
    uint64_t ctr1 = 0;
    while ( !*(B + ctr1) && (ctr1 < m) )
        ctr1++;
    m -= ctr1;
    uint64_t ctr2 = 0;
    while ( !*(A + ctr2) && (ctr2 < n) )
        ctr2++;
    n -= ctr2;

    B = B + ctr1;
    A = A + ctr2;

    /* Check if dividend (A) is 0 */
    if (!n) {
        *ret_len = 1;
        *ret_ptr = calloc(1, sizeof(uint64_t));  // TODO check for NULL return
        return;
    }
    if (n < m) {
        *ret_len = n;
        *ret_ptr = malloc(n * sizeof(uint64_t));     // TODO check for NULL return
        memmove(*ret_ptr, A, n * sizeof(uint64_t));
        for (size_t i = 0; i < *ret_len; i++)
            *(*ret_ptr + i) &= 0x0000000000000001;
        return;
    }

    Poly_Array b = uint64_to_Poly_Array(B + 1, m - 1);
    /* Initialize empty LFSR with length of B */
    Poly_Array lfsr;
    lfsr.deg = m - 2;
    lfsr.len = ceil(1. * (m - 1) / (UINT64_BITS));
    lfsr.poly = calloc(lfsr.len, sizeof(uint64_t));

    /* Move first m coefficients of A into LFSR */
    uint64_t out;
    for (size_t i = 0; i < lfsr.deg; i++) {
        shift_LFSR(&lfsr, &out, (A + i));
    }

    for (size_t i = lfsr.deg; i < n; i++) {
        shift_LFSR(&lfsr, &out, (A + i));
        if (out) {
            for (size_t j = 0; j < lfsr.len; j++) {
                *(lfsr.poly + j) ^= *(b.poly + j);
            }
        }
    }

    uint64_t* ret_tmp = Poly_Array_to_uint64(&lfsr);
    *ret_len = m - 1;

    /* search for highest one coefficient */
    uint64_t ctr3 = 0;
    while(!*(ret_tmp + ctr3))
        ctr3++;
    *ret_len -= ctr3;

    *ret_ptr = malloc(*ret_len * sizeof(uint64_t));
    memmove(*ret_ptr, ret_tmp + ctr3, *ret_len * sizeof(uint64_t));

    free(ret_tmp);
    free(lfsr.poly);
    free(b.poly);
    return;
}


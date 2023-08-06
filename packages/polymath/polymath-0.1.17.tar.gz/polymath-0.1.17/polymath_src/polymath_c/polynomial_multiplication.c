/*
 * This file implements the polynomial_multiplication function from
 * libpolymath.h
 */

#include "libpolymath.h"

void
polynomial_multiplication(const uint64_t* A, uint64_t n,
                          const uint64_t* B, uint64_t m,
                          uint64_t** ret_ptr, uint64_t* ret_len)
{
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

    /* Check if one of the polynomials is 0 */
    if (!n || !m) {
        *ret_len = (uint64_t) 1;
        *ret_ptr = malloc(sizeof(uint64_t));  // TODO check for NULL return
        **ret_ptr = (uint64_t) 0;
        return;
    }
    if (n == 1) { /* Check if A == 1 */
        *ret_len = m;
        *ret_ptr = malloc(sizeof(uint64_t) * m);     // TODO check for NULL return
        memmove(*ret_ptr, B, sizeof(uint64_t) * m);
        for (size_t i = 0; i < m; i++)
            *(*ret_ptr + i) &= 0x0000000000000001;
        return;
    }
    if (m == 1) { /* Check if B == 1 */
        *ret_len = n;
        *ret_ptr = malloc(sizeof(uint64_t) * n);     // TODO check for NULL return
        memmove(*ret_ptr, A, sizeof(uint64_t) * n);
        for (size_t i = 0; i < n; i++)
            *(*ret_ptr + i) &= 0x0000000000000001;
        return;
    }

    /* Determine on which position the input bit is inserted.
     * If the last coefficient equals zero, the last LFSR stage
     * is always filled with zeros. If the last coefficient equals
     * one, the input is always directly shifted into the LFSR.
     */
    uint64_t last_elem = *(B + m - 1);
    Poly_Array b = uint64_to_Poly_Array(B, m - 1);

    /* Initialize empty LFSR with length of B */
    Poly_Array lfsr;
    lfsr.deg = b.deg;
    lfsr.len = ceil(1. * (m - 1) / (UINT64_BITS));
    lfsr.poly = calloc(lfsr.len, sizeof(uint64_t));

    /* Initialize return array */
    *ret_ptr = malloc(sizeof(uint64_t) * (n + m - 1));
    uint64_t ctr = 0;
    /* Shift all the bits of A into the LFSR and perform operations */
    uint64_t out;
    for (size_t i = 0; i < n; i++) {
        /* perform XOR */
        if (*(A + i)) {
            for (size_t j = 0; j < lfsr.len; j++) {
                *(lfsr.poly + j) ^= *(b.poly + j);
            }
        }
        uint64_t in = last_elem * *(A + i);
        shift_LFSR(&lfsr, &out, &in);
        /* set output bit */
        *(*ret_ptr + ctr) = out;
        ctr++;
    }
    /* Shift m - 1 times to empty the LFSR */
    uint64_t in_zero = 0;	// dummy input
    for (size_t i = 0; i < m - 1; i++) {
        shift_LFSR(&lfsr, &out, &in_zero);
        *(*ret_ptr + ctr) = out;
        ctr++;
    }

    /* set length of array */
    *ret_len = n + m - 1;
    free(lfsr.poly);
    free(b.poly);
    return;
}
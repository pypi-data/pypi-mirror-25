/*
 * This file implements the function uint64_to_Poly_Array from libpolymath.h
 */

#include "libpolymath.h"

Poly_Array uint64_to_Poly_Array(const uint64_t* src, uint64_t src_len)
{
    /* Create new Poly_Array */
    Poly_Array poly;
    /* Check for length greater than 0 */
    if (!src_len) {
        poly.len = 0;
        return poly;
    }

    /* Search for leading 1 coefficient */
    uint64_t ctr = 0;
    while (!*(src + ctr))
        ctr++;
    src += ctr;

    poly.deg = src_len - ctr - 1;
    poly.len = ceil(1. * src_len / (UINT64_BITS));
    poly.poly = calloc(poly.len, sizeof(uint64_t));
    if (!poly.poly)
        return poly;

    /* Initialze first bits of the polynomial that don't take the
       space of one whole uint64_t number. */
    uint64_t rem = (src_len - ctr) % (UINT64_BITS);
    if (!rem)
        rem = UINT64_BITS;
    for (size_t i = 0; i < rem; i++) {
        *(poly.poly) ^= (*(src + i) & 0x0000000000000001) << (rem - 1 - i);
    }

    /* Copy the rest of the array into uint64_t numbers */
    for (size_t i = 1; i < poly.len; i++) { // fill Poly_Array parts
        for (size_t j = 0; j < UINT64_BITS; j++) { // read single input bits
            *(poly.poly + i) ^= (*(src + rem) & 0x0000000000000001) << (UINT64_BITS - 1 - j);
            rem++;
        }
    }

    return poly;
}
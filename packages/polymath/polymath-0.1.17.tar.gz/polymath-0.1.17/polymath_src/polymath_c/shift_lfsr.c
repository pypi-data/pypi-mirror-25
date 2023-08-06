/*
 * This file implements the function shift_LFSR from libpolymath.h
 */

#include "libpolymath.h"

void shift_LFSR(Poly_Array* lfsr, uint64_t* out, const uint64_t* in) {
    /* determine output bit of the LFSR */
    uint64_t mask = (uint64_t) 1 << (lfsr->deg % (UINT64_BITS));
    *out = (mask & *(lfsr->poly)) >> (lfsr->deg % (UINT64_BITS));
    /* shift all the data through the array */
    for (size_t i = 0; i < lfsr->len - 1; i++) {
        *(lfsr->poly + i) <<= 1;
        *(lfsr->poly + i) ^= (*(lfsr->poly + i + 1) & 0x8000000000000000)
                >> (UINT64_BITS - 1);
    }
    /* Take the rightmost value of *in and put it in the LFSR */
    *(lfsr->poly + lfsr->len - 1) <<= 1;
    *(lfsr->poly + lfsr->len - 1) ^= (*in & 0x0000000000000001);
}
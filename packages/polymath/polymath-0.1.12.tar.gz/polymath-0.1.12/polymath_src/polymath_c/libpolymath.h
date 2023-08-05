#ifndef POLYMATH_C_LIBRARY_H
#define POLYMATH_C_LIBRARY_H

/* polymathbit.h
 *
 * This file defines the functions and structs for polynomial
 * multiplication and divison over GF(2).
 * The multiplication and division are realized as LFSRs following
 * Saluja, Linear Feedback Shift Registers Theory and Applications, 1987.
 * To enable fast operations we use uint64_t arrays with own functions
 * to realize the sihft over multiple elements of the array.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static const uint64_t UINT64_BITS = sizeof(uint64_t) * 8;

/*
 * The Poly_Array struct represents a univariate polynomial as a bitarray.
 * Each bit represents a coefficient of the polynomial.
 * The array uint64_t* poly contains the coefficients. The most
 * significant coefficient is stored on the leftmost position.
 * The uint64_t len variable contains the number of used
 * uint64_t variables. That means that the number of used bytes
 * corresponds to (sizeof(unit64_t) * len).
 * The uint64_t deg variable stores the degree of the polynomial. So,
 * the number of coefficients equals to (deg + 1).
 */
typedef struct Poly_Array
{
    uint64_t*	poly;
    uint64_t	len;
    uint64_t	deg;
} Poly_Array;


/*
 * Transforms an array of uint64_t numbers into a Poly_Array.
 *
 * The array pointed to by uint64_t* src with length uint64_t src_len
 * is interpreted as a array containing only 0 and 1 and transformed
 * into a Poly_Array. That means that each of the original "bits"
 * now takes exactly one bit space.
 * The Poly_Array is interpreted as a univariate polynomial of
 * length (src_len // (sizeof(uint64_t) * 8) + 1). The degree of the polynomial
 * is the position of the first non-zero entry in the array minus one.
 * Only the rightmost bit of each uint64_t number is used as coefficient.
 *
 * Parameters
 * src      -   pointer to the uint64_t array to transform to a Poly_Array
 * src_len  -   number of elements of src
 *
 * Return value
 * Upon successful transformation uint64_to_Poly_Array returns a
 * a Poly_Array object of the transformed array.
 * If the transformation is not successful a NULL pointer is returned.
 */
Poly_Array uint64_to_Poly_Array(const uint64_t* src, uint64_t src_len);


/*
 * Transforms a Poly_Array into a uint64_t array.
 *
 * Parameters
 * poly - pointer to the Poly_Array that is to be converted into a uint64_t array
 *
 * Return value
 * Returns a pointer to an uint64_t array containing the values of poly
 */
uint64_t* Poly_Array_to_uint64(Poly_Array* poly);


/*
 * Prints all information of a Poly_Array object to stdout.
 */
void print_Poly_Array(Poly_Array* poly);


/*
 * Shifts the LFSR one position to the left.
 *
 * The Poly_Array is interpreted as a LFSR. Shift all the coefficients
 * of the Poly_Array* poly one position to the left and save the
 * output in the variable uint64_t* out. The new input of the LFSR
 * is given by the variable uint64_t* in.
 *
 * Parameters
 * poly -   Pointer to the LFSR
 * out  -   Pointer to the variable that will hold the output of the LFSR.
 *          I.e. the content of the leftmost position before the shift.
 * in   -   Pointer to the new input of the LFSR. The rightmost bit of
 *          the content of in will be the new rightmost bit of the LFSR.
 */
void shift_LFSR(Poly_Array* lfsr, uint64_t* out, const uint64_t* in);


/*
 * Computes the remainder of tow polynomials with 0 padding
 *
 * The first polynomial A is used as the dividend and the second B as the
 * divisor. That means, that there exist polynomials Q and R with
 * deg(R) < deg(B), such that A = Q * B + R.
 * R is computed in the course of the polynomial_modulo_padding function.
 *
 * Parameters
 * A        -   Pointer to the data of the dividend polynomial
 * n        -   Number of elements / coefficients of the dividend
 * B        -   Pointer to the data of the divisor polynomial. If the
 *              divisor is a zero array, the behaviour is undefined.
 * m        -   Number of elements / coefficients of the divisor
 * ret_ptr  -   Address of the pointer to the data of the remainder after
 *              successful completion of the function. The data is filled
 *              with zeros from top. This is useful if the results must
 *              have all the same length.
 * ret_len  -   Number of elements / coefficients of the remainder.
 *              The result array is filled with zeros from top and has
 *              therefore always length (deg(B) - 1).
 */
void
polynomial_modulo_padding(const uint64_t* A, uint64_t n,
                          const uint64_t* B, uint64_t m,
                          uint64_t** ret_ptr, uint64_t* ret_len);


/*
 * Computes the remainder of tow polynomials
 *
 * The first polynomial A is used as the dividend and the second B as the
 * divisor. That means, that there exist polynomials Q and R with
 * deg(R) < deg(B), such that A = Q * B + R.
 * R is computed in the course of the polynomial_modulo_padding function.
 *
 * Parameters
 * A        -   Pointer to the data of the dividend polynomial
 * n        -   Number of elements / coefficients of the dividend
 * B        -   Pointer to the data of the divisor polynomial. If the
 *              divisor is a zero array, the behaviour is undefined.
 * m        -   Number of elements / coefficients of the divisor
 * ret_ptr  -   Address of the pointer to the data of the remainder after
 *              successful completion of the function.
 * ret_len  -   Number of elements / coefficients of the remainder.
 *              The result array is filled with zeros from top and has
 *              therefore always length (deg(B) - 1).
 */
void
polynomial_modulo(const uint64_t* A, uint64_t n,
                  const uint64_t* B, uint64_t m,
                  uint64_t** ret_ptr, uint64_t* ret_len);


/*
 * Multiplies two polynomials.
 *
 * The two input polynomials are multiplied using a LFSR.
 * The second polynomial B is used to determine the feedback coefficients
 * of the LFSR. The polynomial A is step by step shifted into the LFSR
 * and the output is computed.
 * The result of the multiplication is stored at ret and has length
 * ret_len.
 * The position of the leading one-coefficient is for both polynomials,
 * A and B determined. The length of the result depends on the leading 1.
 * If one of the polynomials contains only 0s, i.e. is the zero
 * polynomial, an array of length one containing one 0 is returned.
 *
 * Parameters
 * A        -   Pointer to the first polynomial to multiply
 * n        -   Number of elements in A.
 * B        -   Pointer to the second polynomial to multiply, determines
 *              the coefficients of the LFSR used to multiply.
 * m        -   Number of elements in B.
 * ret_ptr  -   Pointer to the pointer containing the result of
 *              the multiplication.
 * ret_len  -   Resulting number of elements of ret.
 */
void
polynomial_multiplication(const uint64_t* A, uint64_t n,
                          const uint64_t* B, uint64_t m,
                          uint64_t** ret_ptr, uint64_t* ret_len);

/*
 * The dot product of an array with shape (N, k, n) with an
 * array of shape (k, n).
 * The result has shape (N, k)
 */
void
dot(const int64_t* inputs, const double* weights,
    uint64_t n, uint64_t k, uint64_t N,
    double** ret_ptr);

#endif
# polymath: A Python C-Extension Module for Polynomials over GF(2)
![Master Branch Build Status Indicator](https://travis-ci.org/taudor/polymath.svg?branch=master)

polymath is a lightweight and fast C-Extension for python3/numpy for
univariate polynomials with coefficients from the finite field GF(2).
Using bit arithmetic of `uint64_t` variables and the abstract
implementation of Linear Feedback Shift Register enable speed and the
economical use of memory.

polymath builds upon numpy's array type `nd.array` for its communication
with python.

## Installation

### As Python3 Module

polymath requires `numpy` to work correctly.

To install polymath from source simply execute

```
python3 setup.py install
```


### As C Library

polymath uses Cmake and make to create the library file. To compile the
library execute the following steps.

```
cd ./polymath_src/polymath_c/
mkdir ./build
Cmake ./build
cd ./build
make
```

This steps yield the file `libpolymath_c.a` which can be included in
your compile process.

## Usage

### In Python

After successful installation polymath can be imported as a module
in python. The polymath functions can be used in cooperation with
numpys array type `nd.array`. Each function takes one or more arrays
as input and returns one array.

#### Examples

Remember that all coefficients are from the finite field GF(2), i.e.
are either 0 or 1. The following example can be executed in the
python3 console.

```python
>>> import polymath as pm
>>> import numpy as np
>>>
>>> a = np.array([1, 0, 1])
>>> b = np.array([1, 0])
>>> pm.polymul(a, b)
array([1, 0, 1, 0], dtype=uint64)
>>> c = np.array([0, 0, 0, 1, 0])
>>> pm.polymul(a, c)
array([1, 0, 1, 0], dtype=uint64)
```


## In C

After building the library and obtaining the `libpolymath_c.a` file, the
library can be used in C in combination with the header file
`./polymath_src/polymath_c/libpolymath.h`. The result array and the
length variable must be declared before the call to the functions, as in
C the result variables must be given as arguments to the polymath
functions. Note, that you as a caller are responsible to free the
allocated memory by the polymath functions.

### Example

Writing a `test.c` file in the root folder of the project:

```C
#include "./polymath_src/polymath_c/libpolymath.h"

int main()
{
	uint64_t a[] = {1, 0, 1};
	uint64_t b[] = {1, 0, 1, 0, 0, 0, 1, 0, 0};

	uint64_t* res;
	uint64_t res_len;

	polynomial_multiplication(
		a, sizeof(a) / sizeof(uint64_t),
		b, sizeof(b) / sizeof(uint64_t),
		&res, &res_len);

	for (int i = 0; i < res_len; ++i)
	{
		printf("%llu ", *(res + i));
	}
	printf("\n");

	free(res);

	return 0;
}
```

Compile and execute the program with the following commands.

```
$ clang -o test test.c ./polymath_src/polymath_c/cmake-build-debug/libpolymath_c.a
$ ./test
1 0 0 0 1 0 1 0 1 0 0
```


## Tests

The folder `./test/` contains python unittests. To run the tests execute

```
$ python3 -m unittest
```

in your terminal.

## Benchmark

To compare the `polymath` implementation with `numpy` use the
`benchmark.py` file. For help type

```
python3 benchmark.py --help
```

## Help

For help or information about the functions type

```
>>> import polymath
>>> help(polymath)
```

For more detailed information see the documentation in the
`./polymath_src/polymath_c/libpolymath.h` file.
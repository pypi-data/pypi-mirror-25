#include <Python.h>
#include <ndarraytypes.h>
#include <ndarrayobject.h>

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>

#include "polymath_c/libpolymath.h"

static PyObject* 
poly_mul(PyObject *self, PyObject *args)
{
	
	PyObject* in1;
	PyObject* in2;
	PyObject* arr1;
	PyObject* arr2;

	// get arguments
	PyArg_ParseTuple(args, "OO:", &in1, &in2);

	// get np arrays
	arr1 = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
	arr2 = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
	// get length of arrays
	uint64_t* len1 = (uint64_t*) PyArray_DIMS(arr1);
	uint64_t* len2 = (uint64_t*) PyArray_DIMS(arr2);
	// return Py_BuildValue("i", *len1);
	// get data from arrays
	uint64_t* dptr1 = (uint64_t*)(PyArray_DATA(arr1));
	uint64_t* dptr2 = (uint64_t*)(PyArray_DATA(arr2));
	// initialze return arrays
	uint64_t* mult_res;
	uint64_t res_len;

	// perform polynomial division
	polynomial_multiplication(dptr1, *len1, dptr2, *len2, &mult_res, &res_len);
	// dimension of return array, i.e. the number of values
	npy_intp dims[1] = {res_len};
	// create new array to return
	PyObject *ret = PyArray_SimpleNewFromData(1, dims, NPY_UINT64, mult_res);
	// increment counter, so that the memory is not freed
	Py_INCREF(ret);
	// forward the responsibility of the free to numpy
	PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);

	return ret;
}


static PyObject* 
poly_mod_pad(PyObject *self, PyObject *args)
{
	PyObject* in1;
	PyObject* in2;
	PyObject* arr1;
	PyObject* arr2;

	// get arguments
	PyArg_ParseTuple(args, "OO:", &in1, &in2);

	// get np arrays
	arr1 = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
	arr2 = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
	// get length of arrays
	uint64_t* len1 = (uint64_t*) PyArray_DIMS(arr1);
	uint64_t* len2 = (uint64_t*) PyArray_DIMS(arr2);
	// return Py_BuildValue("i", *len1);
	// get data from arrays
	uint64_t* dptr1 = (uint64_t*)(PyArray_DATA(arr1));
	uint64_t* dptr2 = (uint64_t*)(PyArray_DATA(arr2));
	// initialze return arrays
	uint64_t* mod_res;
	uint64_t res_len;

	// perform polynomial division
	polynomial_modulo_padding(dptr1, *len1, dptr2, *len2, &mod_res, &res_len);
	// print_int_array(lfsr, m);

	// dimension of return array, i.e. the number of values
	npy_intp dims[1] = {res_len};
	// create new array to return
	PyObject *ret = PyArray_SimpleNewFromData(1, dims, NPY_UINT64, mod_res);
	// increment counter, so that the memory is not freed
	Py_INCREF(ret);
	// forward the responsibility of the free to numpy
	PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
	
	return ret;
}

static PyObject* 
poly_mod(PyObject *self, PyObject *args)
{
	PyObject* in1;
	PyObject* in2;
	PyObject* arr1;
	PyObject* arr2;

	// get arguments
	PyArg_ParseTuple(args, "OO:", &in1, &in2);

	// get np arrays
	arr1 = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
	arr2 = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
	// get length of arrays
	uint64_t* len1 = (uint64_t*) PyArray_DIMS(arr1);
	uint64_t* len2 = (uint64_t*) PyArray_DIMS(arr2);
	// return Py_BuildValue("i", *len1);
	// get data from arrays
	uint64_t* dptr1 = (uint64_t*)(PyArray_DATA(arr1));
	uint64_t* dptr2 = (uint64_t*)(PyArray_DATA(arr2));
	// initialze return arrays
	uint64_t* mod_res;
	uint64_t res_len;

	// perform polynomial division
	polynomial_modulo(dptr1, *len1, dptr2, *len2, &mod_res, &res_len);
	// print_int_array(lfsr, m);

	// dimension of return array, i.e. the number of values
	npy_intp dims[1] = {res_len};
	// create new array to return
	PyObject *ret = PyArray_SimpleNewFromData(1, dims, NPY_UINT64, mod_res);
	// increment counter, so that the memory is not freed
	Py_INCREF(ret);
	// forward the responsibility of the free to numpy
	PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
	
	return ret;
}

static PyObject* 
poly_dot(PyObject *self, PyObject *args)
{
	PyObject* in1;
	PyObject* in2;
	PyObject* arr1;
	PyObject* arr2;

	// get arguments
	PyArg_ParseTuple(args, "OO:", &in1, &in2);

	// get np arrays
	arr1 = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
	arr2 = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
	// get dimension of inputs, i.e. N, k, n
	uint64_t* dim = (uint64_t*) PyArray_DIMS(arr1);
	uint64_t N = *(dim);
	uint64_t k = *(dim + 1);
	uint64_t n = *(dim + 2);
	
	// get data from arrays
	int64_t* dptr1 = (int64_t*) (PyArray_DATA(arr1));
	double* dptr2 = (double*) (PyArray_DATA(arr2));
	// initialze return arrays
	double* dot_res;

	// perform polynomial division
	dot(dptr1, dptr2, n, k, N, &dot_res);
	// print_int_array(lfsr, m);

	// dimension of return array, i.e. the number of values
	npy_intp dims[2] = {N, k};
	// create new array to return
	PyObject *ret = PyArray_SimpleNewFromData(2, dims, NPY_DOUBLE, dot_res);
	// increment counter, so that the memory is not freed
	Py_INCREF(ret);
	// forward the responsibility of the free to numpy
	PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
	
	return ret;
}

static PyObject* 
poly_eval_id_xor(PyObject *self, PyObject *args)
{
	PyObject* in1;
	PyObject* in2;
	PyObject* arr1;
	PyObject* arr2;

	// get arguments
	PyArg_ParseTuple(args, "OO:", &in1, &in2);

	// get np arrays
	arr1 = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
	arr2 = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
	// get dimension of inputs, i.e. N, k, n
	uint64_t* dim = (uint64_t*) PyArray_DIMS(arr1);
	uint64_t N = *(dim);
	uint64_t n = *(dim + 1);
	uint64_t* dim_weights = (uint64_t*) PyArray_DIMS(arr2);
	uint64_t k = *(dim_weights);
	
	// get data from arrays
	int64_t* dptr1 = (int64_t*) (PyArray_DATA(arr1));
	double*  dptr2 = (double*) (PyArray_DATA(arr2));
	// initialze return arrays
	int64_t* res;

	// perform polynomial division
	eval_id_xor(dptr1, dptr2, n, k, N, &res);
	// return Py_BuildValue("i", k);

	// dimension of return array, i.e. the number of values
	npy_intp dims[1] = {N};
	// create new array to return
	PyObject *ret = PyArray_SimpleNewFromData(1, dims, NPY_INT64, res);
	// increment counter, so that the memory is not freed
	Py_INCREF(ret);
	// forward the responsibility of the free to numpy
	PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
	
	return ret;
}

/* Python documentation for functions */
PyDoc_STRVAR(
    polymul_doc,
    "polymul(mul1, mul2)\n"
    "--\n\n"
    "Multiplication of two polynomials.\n\n"
    "Parameters\n"
    "----------\n"
    "mul1 : array_like\n"
    "\tFirst multiplicand.\n"
    "mul2 : array_like\n"
    "\tSecond multiplicand.");

PyDoc_STRVAR(
    polymodpad_doc,
    "polymodpad(divd, divs)\n"
    "--\n\n"
    "Remainder of two polynomials with 0 padding.\n\n"
    "Using the first argument as dividend and the second as\n"
    "divisor, the remainder of the division is computed.\n"
    "That means, there exist polynomials Q and R with deg(R) < deg(divs)\n"
    "such that the equation divd = Q * divs + R is fullfilled.\n"
    "R is returned as the result of the polymodpad function.\n"
    "The difference to the function polymod is that in this case the response is\n"
    "padded with zeros in the beginning, so that len(R) = len(divs) - 1\n"
    "\n"
    "Parameters\n"
    "----------\n"
    "divd : array_like\n"
    "\tDividend.\n"
    "divs : array_like\n"
    "\tDivisor.");

PyDoc_STRVAR(
    polymod_doc,
    "polymod(divd, divs)\n"
    "--\n\n"
    "Remainder of two polynomials.\n\n"
    "Using the first argument as dividend and the second as\n"
    "divisor, the remainder of the division is computed.\n"
    "That means, there exist polynomials Q and R with deg(R) < deg(divs)\n"
    "such that the equation divd = Q * divs + R is fullfilled.\n"
    "R is returned as the result of the polymodpad function.\n"
    "\n"
    "Parameters\n"
    "----------\n"
    "divd : array_like\n"
    "\tDividend.\n"
    "divs : array_like\n"
    "\tDivisor.");

PyDoc_STRVAR(
    dot_doc,
    "dot(inputs, weights)\n"
    "--\n\n"
    "Dot product of N inputs with weights.\n\n"
    "The fist parameter is of shape (N, k, n) and\n"
    "represents a set of N challenges for a k-Arbiter PUF.\n"
    "The second parameter is of shape (k, n) and represents\n"
    "the weight arrays of a k-Arbiter PUF.\n"
    "The result is an array of shape (N, k) and represents\n"
    "the evaluated real-value challenges with the k-Arbiter PUF.\n"
    "\n"
    "Parameters\n"
    "----------\n"
    "inputs : array_like\n"
    "\tChallenges.\n"
    "weights : array_like\n"
    "\tWeights.\n\n"
    "Return\n"
    "------\n"
    "return: array_like\n"
    "\tEvaluated challenges."
    );

PyDoc_STRVAR(
    eval_id_xor_doc,
    "eval_id_xor(inputs, weights)\n"
    "--\n\n"
    "Evaluate N inputs from given weights.\n\n"
    "The fist parameter is of shape (N, k, n) and\n"
    "represents a set of N challenges for a k-Arbiter PUF.\n"
    "The second parameter is of shape (k, n) and represents\n"
    "the weight arrays of a k-Arbiter PUF.\n"
    "The result is an array of shape (N) and represents\n"
    "the evaluated challenges with the k-Arbiter PUF.\n"
    "\n"
    "Parameters\n"
    "----------\n"
    "inputs : array_like\n"
    "\tChallenges.\n"
    "weights : array_like\n"
    "\tWeights.\n\n"
    "Return\n"
    "------\n"
    "return: array_like\n"
    "\tEvaluated challenges with sign."
    );

PyDoc_STRVAR(
    polymath_doc,
    "polymath is a lightweight and fast C-Extension for \n"
    "python3/numpy for univariate polynomials with coefficients \n"
    "from the finite field GF(2).\n");

static PyMethodDef PolymathMethods[] = {
	{"polymul",  poly_mul, METH_VARARGS, polymul_doc},
	{"polymodpad",  poly_mod_pad, METH_VARARGS, polymodpad_doc},
	{"polymod",  poly_mod, METH_VARARGS, polymod_doc},
	{"dot",  poly_dot, METH_VARARGS, dot_doc},
	{"eval_id_xor",  poly_eval_id_xor, METH_VARARGS, eval_id_xor_doc},
	{NULL, NULL, 0, NULL}		/* Sentinel */
};

static struct PyModuleDef polymathmodule = {
   PyModuleDef_HEAD_INIT,
   "polymath",   /* name of module */
   polymath_doc, /* module documentation, may be NULL */
   -1,	   /* size of per-interpreter state of the module,
				or -1 if the module keeps state in global variables. */
   PolymathMethods
};

PyMODINIT_FUNC PyInit_polymath(void)
{
	// call to be able to create ndarrays
	_import_array();
	return PyModule_Create(&polymathmodule);
}
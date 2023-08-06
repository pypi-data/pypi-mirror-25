#include <Python.h>
#include <numpy/ndarraytypes.h>
#include <numpy/ndarrayobject.h>

#include "pypuf_helper.h"

static PyObject* 
eval_id_xor_wrapper(PyObject *self, PyObject *args)
{
    PyObject* in1;
    PyObject* in2;
    PyObject* challenges;
    PyObject* weights;

    // get arguments
    PyArg_ParseTuple(args, "OO:", &in1, &in2);

    // get np arrays
    challenges = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
    weights = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
    // get dimension of inputs, i.e. N, k, n
    uint64_t* dim_c = (uint64_t*) PyArray_DIMS(challenges);
    uint64_t* dim_w = (uint64_t*) PyArray_DIMS(weights);

    uint64_t N_c = *(dim_c);
    uint64_t n_c = *(dim_c + 1);
    
    uint64_t k_w = *(dim_w);
    uint64_t n_w = *(dim_w + 1);

    //check if the array shapes match
    if (n_c - n_w)
        return Py_BuildValue("i", -2);
    
    // get data from arrays
    int64_t* dptr_c = (int64_t*) (PyArray_DATA(challenges));
    double*  dptr_w = (double*) (PyArray_DATA(weights));
    // initialze return arrays
    int64_t* res = NULL;

    // perform polynomial division
    eval_id_xor(dptr_c, dptr_w, n_w, k_w, N_c, &res);
    // dimension of return array, i.e. the number of values
    npy_intp dims[1] = {N_c};
    // create new array to return
    PyObject *ret = PyArray_SimpleNewFromData(1, dims, NPY_INT64, res);
    // increment counter, so that the memory is not freed
    Py_INCREF(ret);
    // forward the responsibility of the free to numpy
    PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
    
    return ret;
}

static PyObject* 
eval_sign_wrapper(PyObject *self, PyObject *args)
{
    PyObject* in1;
    PyObject* in2;
    PyObject* challenges;
    PyObject* weights;

    // get arguments
    PyArg_ParseTuple(args, "OO:", &in1, &in2);

    // get np arrays
    challenges = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
    weights = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
    // get dimension of inputs, i.e. N, k, n
    uint64_t* dim_c = (uint64_t*) PyArray_DIMS(challenges);
    uint64_t* dim_w = (uint64_t*) PyArray_DIMS(weights);

    uint64_t N_c = *(dim_c);
    uint64_t k_c = *(dim_c + 1);
    uint64_t n_c = *(dim_c + 2);

    uint64_t k_w = *(dim_w);
    uint64_t n_w = *(dim_w + 1);

    //check if the array shapes match
    if (n_c - n_w)
        return Py_BuildValue("i", -2); // TODO what return value?
    if (k_c - k_w)
        return Py_BuildValue("i", -2);
    
    // get data from arrays
    int64_t* dptr_c = (int64_t*) (PyArray_DATA(challenges));
    double*  dptr_w = (double*) (PyArray_DATA(weights));
    // initialze return arrays
    int64_t* res = NULL;

    // perform polynomial division
    eval_sign(dptr_c, dptr_w, n_w, k_w, N_c, &res);
    // dimension of return array, i.e. the number of values
    npy_intp dims[2] = {N_c, k_c};
    // create new array to return
    PyObject *ret = PyArray_SimpleNewFromData(2, dims, NPY_INT64, res);
    // increment counter, so that the memory is not freed
    Py_INCREF(ret);
    // forward the responsibility of the free to numpy
    PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
    
    return ret;
}

static PyObject* 
eval_wrapper(PyObject *self, PyObject *args)
{
    PyObject* in1;
    PyObject* in2;
    PyObject* challenges;
    PyObject* weights;

    // get arguments
    PyArg_ParseTuple(args, "OO:", &in1, &in2);

    // get np arrays
    challenges = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
    weights = PyArray_FROM_OTF(in2, NPY_NOTYPE, NPY_IN_ARRAY);
    // get dimension of inputs, i.e. N, k, n
    uint64_t* dim_c = (uint64_t*) PyArray_DIMS(challenges);
    uint64_t* dim_w = (uint64_t*) PyArray_DIMS(weights);

    uint64_t N_c = *(dim_c);
    uint64_t k_c = *(dim_c + 1);
    uint64_t n_c = *(dim_c + 2);

    uint64_t k_w = *(dim_w);
    uint64_t n_w = *(dim_w + 1);

    //check if the array shapes match
    if (n_c - n_w)
        return Py_BuildValue("i", -2); // TODO what return value?
    if (k_c - k_w)
        return Py_BuildValue("i", -2);
    
    // get data from arrays
    int64_t* dptr_c = (int64_t*) (PyArray_DATA(challenges));
    double*  dptr_w = (double*) (PyArray_DATA(weights));
    // initialze return arrays
    double* res = NULL;

    // perform polynomial division
    eval(dptr_c, dptr_w, n_w, k_w, N_c, &res);
    // dimension of return array, i.e. the number of values
    npy_intp dims[2] = {N_c, k_c};
    // create new array to return
    PyObject *ret = PyArray_SimpleNewFromData(2, dims, NPY_DOUBLE, res);
    // increment counter, so that the memory is not freed
    Py_INCREF(ret);
    // forward the responsibility of the free to numpy
    PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
    
    return ret;
}

static PyObject* 
combiner_xor_wrapper(PyObject *self, PyObject *args)
{
    PyObject* in1;
    PyObject* challenges;

    // get arguments
    PyArg_ParseTuple(args, "O:", &in1);

    // get np array
    challenges = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
    // get dimension of inputs, i.e. N, k
    uint64_t* dim = (uint64_t*) PyArray_DIMS(challenges);
    uint64_t N = *(dim);    
    uint64_t k = *(dim + 1);
    
    // get data from array
    int64_t* dptr_c = (int64_t*) (PyArray_DATA(challenges));
    // initialze return array
    int64_t* res = NULL;

    // perform polynomial division
    combiner_xor(dptr_c, k, N, &res);
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

static PyObject* 
transform_id_wrapper(PyObject *self, PyObject *args)
{
    PyObject* in1;
    PyObject* challenges;
    uint64_t k;

    // get arguments
    PyArg_ParseTuple(args, "Ok:", &in1, &k);

    // get np array
    challenges = PyArray_FROM_OTF(in1, NPY_NOTYPE, NPY_IN_ARRAY);
    // get dimension of inputs, i.e. N, k
    uint64_t* dim = (uint64_t*) PyArray_DIMS(challenges);
    uint64_t N = *(dim);    
    uint64_t n = *(dim + 1);
    
    // get data from array
    int64_t* dptr_c = (int64_t*) (PyArray_DATA(challenges));
    // initialze return array
    int64_t* res = NULL;

    // perform polynomial division
    transform_id(dptr_c, n, k, N, &res);
    // dimension of return array, i.e. the number of values
    npy_intp dims[3] = {N, k, n};
    // create new array to return
    PyObject *ret = PyArray_SimpleNewFromData(3, dims, NPY_INT64, res);
    // increment counter, so that the memory is not freed
    Py_INCREF(ret);
    // forward the responsibility of the free to numpy
    PyArray_ENABLEFLAGS((PyArrayObject*)ret, NPY_ARRAY_OWNDATA);
    
    return ret;
}

PyDoc_STRVAR(
    eval_sign_doc,
    "eval_sign(challenges, weights)\n"
    "--\n"
    "The function eval takes as input a set of N transformed challenges\n"
    "for an n-bit k-Arbiter PUF. That means that the input should have\n"
    "shape (N, k, n). This set of challenges is evaluated with an\n"
    "n-bit k-Arbiter PUF and the individual responses for each Aribter\n"
    "Chain are created taking the sign of each response.\n\n"
    "Parameters\n"
    "----------\n"
    "challenges : array_like\n"
    "\tSet of already transformed challenges of shape (N, k, n).\n"
    "weights: array_like\n"
    "\tThe weight array of the k-Ariber PUF of shape (k, n).\n"
    "Return\n"
    "------\n"
    "subresults: arral_like\n"
    "\tEvaluated and signed results of the challenges for each Arbiter Chain.\n"
    "\tHas shape (N, k).\n"
    );

PyDoc_STRVAR(
    eval_doc,
    "eval(challenges, weights)\n"
    "--\n"
    "The function eval takes as input a set of N transformed challenges\n"
    "for an n-bit k-Arbiter PUF. That means that the input should have\n"
    "shape (N, k, n). This set of challenges is evaluated with an\n"
    "n-bit k-Arbiter PUF and the individual responses for each Aribter\n"
    "Chain are created.\n\n"
    "Parameters\n"
    "----------\n"
    "challenges : array_like\n"
    "\tSet of already transformed challenges of shape (N, k, n).\n"
    "weights: array_like\n"
    "\tThe weight array of the k-Ariber PUF of shape (k, n).\n"
    "Return\n"
    "------\n"
    "subresults: arral_like\n"
    "\tEvaluated results of the challenges for each Arbiter Chain.\n"
    "\tHas shape (N, k).\n"
    );

PyDoc_STRVAR(
    combiner_xor_doc,
    "combiner_xor(subresults)\n"
    "--\n"
    "The function takes a set of evaluated responses from the individual\n"
    "Arbiter Chains of shape (N, k) and XORs the results to the final\n"
    "result of the k-XOR Arbiter PUF.\n\n"
    "Parameters\n"
    "----------\n"
    "subresults : array_like\n"
    "\tSet of subresults of shape (N, k).\n"
    "Return\n"
    "------\n"
    "evaluated_subresults: arral_like\n"
    "\tXORed results of the subchallenges of shape (N).\n"
    );

PyDoc_STRVAR(
    transform_id_doc,
    "transform_id(challenges, k)\n"
    "--\n\n"
    "Transforms a set of N challenges of bitlength n into a set of\n"
    "challenges for a k-Arbiter PUF, so that each subchallenge is\n"
    "the same.\n"
    "The result has shape (N, k, n).\n\n"
    "Parameters\n"
    "----------\n"
    "challenges : array_like\n"
    "\tSet of challenges of shape (N, n).\n"
    "k : int\n"
    "\tNumber of Arbiter Chains in the k-Arbiter PUF.\n"
    "Return\n"
    "------\n"
    "transformed_challenges: arral_like\n"
    "\tTransformed challenges with the id-transform. Each subchallenge is the\n"
    "\tsame. The array has shape (N, k, n).\n"
    );

PyDoc_STRVAR(
    eval_id_xor_doc,
    "eval_id_xor(challenges, weights)\n"
    "--\n\n"
    "Evaulates a set of N challenges with the id transformation,\n"
    "i.e. the challenge set is extended so that each subchallenge\n"
    "is the same.\n"
    "The challenges will be evaluated on a k-XOR Arbiter PUF of length n.\n" 
    "The values of the shape of the challenge set and the Arbiter PUFs are\n"
    "determined from the numpy arrays.\n"
    "The result of the evaluated challenges has shape (N).\n\n"
    "Parameters\n"
    "----------\n"
    "challenges : array_like\n"
    "\tSet of challenges of shape (N, n).\n"
    "weights : array_like\n"
    "\tWeight array of the k-XOR Aribter PUF. The array has shape (k, n).\n"
    "Return\n"
    "------\n"
    "evaluated_subresults: arral_like\n"
    "\tEvaluated and XORed results of the challenges of shape (N).\n"
    );

PyDoc_STRVAR(
    pypuf_helper_doc,
    "pypuf_helper contains helper functions for the pypuf \n"
    "learning framework for PUFs.\n");

static PyMethodDef pypuf_helperMethods[] = {
    {"eval_id_xor",  eval_id_xor_wrapper, METH_VARARGS, eval_id_xor_doc},
    {"eval_sign",  eval_sign_wrapper, METH_VARARGS, eval_sign_doc},
    {"eval",  eval_wrapper, METH_VARARGS, eval_doc},
    {"combiner_xor",  combiner_xor_wrapper, METH_VARARGS, combiner_xor_doc},
    {"transform_id",  transform_id_wrapper, METH_VARARGS, transform_id_doc},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef pypuf_helpermodule = {
   PyModuleDef_HEAD_INIT,
   "pypuf_helper",   /* name of module */
   pypuf_helper_doc, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   pypuf_helperMethods
};

PyMODINIT_FUNC PyInit_pypuf_helper(void)
{
    // call to be able to create ndarrays
    _import_array();
    return PyModule_Create(&pypuf_helpermodule);
}
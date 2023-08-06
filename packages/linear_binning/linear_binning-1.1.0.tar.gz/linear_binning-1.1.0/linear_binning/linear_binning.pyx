# distutils: language = c++
# distutils: sources = linear_binning/linear_binning_impl.cpp
# distutils: libraries = ["m"]

import numpy as np
cimport numpy as np
#from libcpp cimport double
#from libcpp cimport uint64

cdef extern from "linear_binning_impl.hpp":
    void linear_binning_impl(const unsigned long D,
                             const double *X,
                             const double *weights,
                             const unsigned long n_samples,
                             const double *extents,
                             const double *bin_sizes,
                             const unsigned long *sizes,
                             double *result_X,
                             double *result_weights)

def cython_linear_binning (np.ndarray[double, ndim=2, mode='c'] X,
                           np.ndarray[double, ndim=1, mode='c'] weights,
                           np.ndarray[double, ndim=2, mode='c'] extents,
                           np.ndarray[unsigned long, ndim=1, mode='c'] sizes):
    """Performs a linear binning on weighted data

    This algorithm is able to operate on N data point in D dimensions and
    produces a number of grid points, G=sizes.prod(), with their corresponding
    weights.
    The input arrays need to be c-contiguous and strictly adhere to the
    required types (double and unsigned long).

    Parameters
    ----------
    X : 2D numpy array with shape (N, D) of type double
        data coordinates
    weights : 1D numpy array with shape (N) of type double
        data weights
    extents : 2D numpy array with shape (D, 2) of type double
        limits of grid (all data outside this rectangular region is under- or
        overflow)
    sizes : 1D numpy array with shape (D) of type unsigned long
        number of bin centers (grid points) in each dimension

    Returns
    -------
    2D numpy array with shape (G, D) of type double
        grid points
    1D numpy array with shape (N) of type double
        weights at the corresponding grid points
    """
    assert X.shape[0] == weights.size   # these must be the number of data points
    assert X.shape[1] == extents.shape[0] == sizes.size  # these must be the dimension
    assert extents.shape[1] == 2

    cdef unsigned long n_samples = X.shape[0]
    cdef unsigned long D = X.shape[1]
    cdef np.ndarray[double, ndim = 2, mode = 'c'] result_X = \
        np.empty((sizes.prod(), D))
    cdef np.ndarray[double, ndim = 1, mode = 'c'] result_weights = \
        np.zeros((sizes.prod()))
    cdef np.ndarray[double, ndim = 1, mode = 'c'] bin_sizes = \
        np.empty(D, np.dtype('d'))

    bin_sizes = (np.abs(np.diff(extents, axis=1).T)/(sizes - 1)).flatten(order='C')

    linear_binning_impl(D, &X[0, 0], &weights[0], n_samples,
                        &extents[0, 0], &bin_sizes[0], &sizes[0],
                        &result_X[0, 0], &result_weights[0])

    return result_X, result_weights

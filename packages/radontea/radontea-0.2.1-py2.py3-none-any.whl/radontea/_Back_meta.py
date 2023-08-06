#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    _Back.py

    The inverse Radon transform with non-iterative techniques.
"""

from __future__ import division

import sys

from . import _Back as back2d
from . import _Back_iterative as back2d_it
from . import _Back_3D as back3d

__all__ = back2d.__all__ + back2d_it.__all__


def art(sinogram, angles, initial=None, iterations=1,
        jmc=None, jmm=None):
    u""" Algebraic Reconstruction Technique

    The Algebraic Reconstruction Technique (ART) iteratively
    computes the inverse of the Radon transform in two dimensions.
    The reconstruction technique uses *rays* of the diameter of
    one pixel to iteratively solve the system of linear equations
    that describe the projection process. The binary weighting
    factors are

     - 1, if the center of the a pixel is within the *ray*
     - 0, else


    Parameters
    ----------
    sinogram : ndarray, shape (A,N) or (A,M,N)
        Two- or three-dimensional sinogram of line recordings. If the
        sinogram is three-dimensional, the dimension `M` iterates 
        through the slices. The rotation takes place through
        the second (y) axis.
    angles : ndarray, length A
        Angular positions of the `sinogram` in radians. The angles
        at which the sinogram slices were recorded do not have to be
        distributed equidistantly as in :func:`backproject`.
        The angles are internaly converted to modulo PI.
    initial : ndarray, shape (N,N) or (N,M,N), optional
        The initial guess for the solution.
    iterations : int
        Number of iterations to perform.
    jmc, jmm : instance of :func:`multiprocessing.Value` or `None`
        The progress of this function can be monitored with the 
        :mod:`jobmanager` package. The current step `jmc.value` is
        incremented `jmm.value` times. `jmm.value` is set at the 
        beginning.


    Returns
    -------
    out : ndarray, shape (N,N) or (N,M,N)
        The reconstructed image.


    See Also
    --------
    sart : simultaneous algebraic reconstruction technique


    Notes
    -----
    For theoretical backround, see
    Kak, A. C., & Slaney, M.. *Principles of Computerized
    Tomographic Imaging*, SIAM, (2001)

    Sec. 7.2:
    *"ART reconstrutions usually suffer from salt and pepper noise,
    which is caused by the inconsitencies introuced in the set of
    equations by the approximations commonly used for* 
    :math:`w_{ik}` *'s."*
    """
    # This is a convenience function that wraps 2d and 3d
    # collect all arguments
    code = sys._getframe().f_code
    keys = code.co_varnames[:code.co_argcount]
    kwargs = dict()
    lcs = locals()
    for key in list(keys):
        kwargs[key] = lcs[key]

    return two_three_dim_recon(code, kwargs)


def backproject(sinogram, angles, filtering="ramp",
                padding=True, padval=0,
                jmc=None, jmm=None, verbose=0):
    u""" Backprojection with the Fourier slice theorem

    Computes the inverse of the radon transform using filtered
    backprojection.


    Parameters
    ----------
    sinogram : ndarray, shape (A,N) or (A,M,N)
        Two- or three-dimensional sinogram of line recordings. If the
        sinogram is three-dimensional, the dimension `M` iterates 
        through the slices. The rotation takes place through
        the second (y) axis.
    angles : (A,) ndarray
        Angular positions of the `sinogram` in radians equally
        distributed from zero to PI.
    filtering : {'ramp', 'shepp-logan', 'cosine', 'hamming', \
                 'hann'}, optional
        Specifies the Fourier filter. Either of

          - "ramp": mathematically correct reconstruction
          - "shepp-logan"
          - "cosine"
          - "hamming"
          - "hann"

    padding : bool, optional
        Pad the input data to the second next power of 2 before
        Fourier transforming. This reduces artifacts and speeds up
        the process for input image sizes that are not powers of 2.
    padval : float
        The value used for padding.
        If `padval` is `None`, then the edge values are used for
        padding (see documentation of `numpy.pad`).
    jmc, jmm : instance of :func:`multiprocessing.Value` or `None`
        The progress of this function can be monitored with the 
        :mod:`jobmanager` package. The current step `jmc.value` is
        incremented `jmm.value` times. `jmm.value` is set at the 
        beginning.
    verbose : int
        Increment to increase verbosity.


    Returns
    -------
    out : ndarray, shape (N,N) or (N,M,N)
        The reconstructed image.


    Examples
    --------
    >>> import numpy as np
    >>> from radontea import backproject
    >>> N = 5
    >>> A = 7
    >>> x = np.linspace(-N/2, N/2, N)
    >>> projection = np.exp(-x**2)
    >>> sinogram = np.tile(projection, A).reshape(A,N)
    >>> angles = np.linspace(0, np.pi, A, endpoint=False)
    >>> backproject(sinogram, angles)
    array([[ 0.03768159, -0.02020189, -0.02287825,  0.03766525,  0.01771381],
           [ 0.03945197, -0.01662539,  0.02187192,  0.04124174,  0.0194842 ],
           [ 0.02491933,  0.11287706,  0.41412685,  0.17074419,  0.00495156],
           [ 0.03915731,  0.10966977,  0.27540441,  0.16753691,  0.01918954],
           [ 0.02052438,  0.03156967,  0.07341154,  0.08943681,  0.0005566 ]])


    See Also
    --------
    fourier_map : implementation by Fourier interpolation
    sum : implementation by summation in real space
    """
    # This is a convenience function that wraps 2d and 3d
    # collect all arguments
    code = sys._getframe().f_code
    keys = code.co_varnames[:code.co_argcount]
    kwargs = dict()
    lcs = locals()
    for key in list(keys):
        kwargs[key] = lcs[key]

    return two_three_dim_recon(code, kwargs)


def fourier_map(sinogram, angles, intp_method="cubic",
                jmc=None, jmm=None):
    u""" Fourier mapping with the Fourier slice theorem

    Computes the inverse of the radon transform using Fourier
    interpolation.
    Warning: This is the naive reconstruction that assumes that
    the image is rotated through the upper left pixel nearest to
    the actual center of the image. We do not have this problem for
    odd images, only for even images.


    Parameters
    ----------
    sinogram : ndarray, shape (A,N) or (A,N,M)
        Two- or three-dimensional sinogram of line recordings. If the
        sinogram is three-dimensional, the dimension `M` iterates 
        through the slices. The rotation takes place through
        the second (y) axis.
    angles : (A,) ndarray
        Angular positions of the `sinogram` in radians equally
        distributed from zero to PI.
    intp_method : {'cubic', 'nearest', 'linear'}, optional
        Method of interpolation. For more information see
        `scipy.interpolate.griddata`. One of

          - "nearest": instead of interpolating, use the points closest
            to the input data
          - "linear": bilinear interpolation between data points
          - "cubic": interpolate using a two-dimensional poolynimial
            surface

    jmc, jmm : instance of :func:`multiprocessing.Value` or `None`
        The progress of this function can be monitored with the 
        :mod:`jobmanager` package. The current step `jmc.value` is
        incremented `jmm.value` times. `jmm.value` is set at the 
        beginning.


    Returns
    -------
    out : ndarray, shape (N,N) or (N,M,N)
        The reconstructed image.


    See Also
    --------
    backproject : implementation by backprojection
    sum : implementation by summation in real space
    scipy.interpolate.griddata : the used interpolation method
    """
    # This is a convenience function that wraps 2d and 3d
    # collect all arguments
    code = sys._getframe().f_code
    keys = code.co_varnames[:code.co_argcount]
    kwargs = dict()
    lcs = locals()
    for key in list(keys):
        kwargs[key] = lcs[key]

    return two_three_dim_recon(code, kwargs)


def sart(sinogram, angles, initial=None, iterations=1,
         jmc=None, jmm=None):
    u""" Simultaneous Algebraic Reconstruction Technique


    SART computes an inverse of the Radon transform in two dimensions.
    The reconstruction technique uses "rays" of the diameter of
    one pixel to iteratively solve the system of linear equations
    that describe the image. The weighting factors are bilinear
    elements. At the beginning and end of each ray, only partial
    weights are used. The pixel values of the image are updated
    only after each iteration is complete.


    Parameters
    ----------
    sinogram : ndarray, shape (A,N) or (A,M,N)
        Two- or three-dimensional sinogram of line recordings. If the
        sinogram is three-dimensional, the dimension `M` iterates 
        through the slices. The rotation takes place through
        the second (y) axis.
    angles : ndarray, length A
        Angular positions of the `sinogram` in radians. The angles
        at which the sinogram slices were recorded do not have to be
        distributed equidistantly as in backprojection techniques.
        The angles are internaly converted to modulo PI.
    initial : ndarray, shape (N,N) or (N,M,N), optional
        The initial guess for the solution.
    iterations : integer
        Number of iterations to perform.
    jmc, jmm : instance of :func:`multiprocessing.Value` or `None`
        The progress of this function can be monitored with the 
        :mod:`jobmanager` package. The current step `jmc.value` is
        incremented `jmm.value` times. `jmm.value` is set at the 
        beginning.


    Returns
    -------
    out : ndarray, shape (N,N) or (N,M,N)
        The reconstructed image.


    See Also
    --------
    art : algebraic reconstruction technique


    Notes
    -----
    Algebraic reconstruction technique (ART) (see `art`):
        Iterations are performed over each ray of each projection.
        Weighting factors are binary (1 if center of pixel is
        within ray, 0 else). This leads to salt and pepper noise.

    Simultaneous iterative reconstruction technique (SIRT):
        Same idea as ART, but for each iteration, the change of the
        image f is computed for all rays and projections separately
        and the weights are applied simultaneously after each
        iteration. The result is a slower convergence but the final
        image is also less noisy.

    This implementation does NOT use a hamming window to filter
    the data and to emphasize points at the center of the recon-
    struction region.

    For theoretical backround, see
    Kak, A. C., & Slaney, M.. *Principles of Computerized
    Tomographic Imaging*, SIAM, (2001)

    Sec 7.4:
    *"[SART] seems to combine the best of ART and SIRT. [...] Here
    are the main features if SART: First, [...] the traditional
    pixel basis is abandonded in favor of bilinear elements
    [e.g. interpolation]. Also, for a circular reconstruction
    region, only partial weights are assigned to the first and last
    picture elements on the individual rays. To further reduce the
    noise [...], the correction terms are simultaneously applied
    for all the rays in one projection [...]."*
    """
    # This is a convenience function that wraps 2d and 3d
    # collect all arguments
    code = sys._getframe().f_code
    keys = code.co_varnames[:code.co_argcount]
    kwargs = dict()
    lcs = locals()
    for key in list(keys):
        kwargs[key] = lcs[key]

    return two_three_dim_recon(code, kwargs)


def sum(sinogram, angles, jmc=None, jmm=None):  # @ReservedAssignment
    u""" Sum-reconstruction with the Fourier slice theorem

    Computes the inverse of the radon transform by computing the
    integral in real space.

    .. warning:: This algorithm is slow and prone to numerical errors.
    
    Parameters
    ----------
    sinogram : ndarray, shape (A,N) or (A,M,N)
        Two- or three-dimensional sinogram of line recordings. If the
        sinogram is three-dimensional, the dimension `M` iterates 
        through the slices. The rotation takes place through
        the second (y) axis.
    angles : (A,) ndarray
        Angular positions of the `sinogram` in radians equally 
        distributed from zero to PI.
    jmc, jmm : instance of :func:`multiprocessing.Value` or `None`
        The progress of this function can be monitored with the 
        :mod:`jobmanager` package. The current step `jmc.value` is
        incremented `jmm.value` times. `jmm.value` is set at the 
        beginning.



    Returns
    -------
    out : ndarray, shape (N,N) or (N,M,N)
        The reconstructed image.


    See Also
    --------
    backproject : implementation by backprojection
    fourier_map : implementation by summation in real space
    """
    # This is a convenience function that wraps 2d and 3d
    # collect all arguments
    code = sys._getframe().f_code
    keys = code.co_varnames[:code.co_argcount]
    kwargs = dict()
    lcs = locals()
    for key in list(keys):
        kwargs[key] = lcs[key]

    return two_three_dim_recon(code, kwargs)


def two_three_dim_recon(code, kwargs):
    sinogram = kwargs["sinogram"]

    if len(sinogram.shape) == 2:
        # 2D
        if hasattr(back2d, code.co_name):
            func = getattr(back2d, code.co_name)
        elif hasattr(back2d_it, code.co_name):
            func = getattr(back2d_it, code.co_name)
        else:
            raise NotImplementedError("Unknown method: ", code.co_name)
    elif len(sinogram.shape) == 3:
        # 3D
        if hasattr(back3d, code.co_name):
            func = getattr(back3d, code.co_name)
        else:
            raise NotImplementedError("Unknown method: ", code.co_name)
    else:
        raise ValueError("sinogram must have dimension 2 or 3.")

    return func(**kwargs)

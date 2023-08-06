from __future__ import division
import numpy
from numpy.fft import rfft, hfft


class multj(object):
    r"""Compute integrals with multiple spherical Bessel functions of integer orders

    .. math:: G(y_0, ..., y_{m-1}) = \int_0^\infty
        F(x) \prod_{i=0}^{m-1} j_{n_i}(xy_i) \,\frac{\mathrm{d}x}x

    It expands the product of :math:`j_n` in sines and cosines using
    product-to-sum identities, transform each terms before combining them [1]_.

    Parameters
    ----------
    x : float, array_like
        log-evenly spaced input argument
    n : int, array_like
        nonnegative integer orders of the spherical Bessel functions
    q : float
        "top-level" power-law tilt

    Attributes
    ----------
    x : float, array_like
        log-evenly spaced input argument
    y : float, array_like
        XXXXXXXXXXXXXXXXXXX
    prefac : float, array_like
        factor to multiply before the transform, serves to convert an integral
        to the general form (apart from the tilt factor :math:`x^{-q}`)
    postfac : float, array_like
        factor to multiply after the transform, serves to convert an integral
        to the general form (apart from the tilt factor :math:`y^{-q}`)

    Methods
    -------
    __call__

    Examples
    --------

    References
    ----------
    .. [1] Our paper
    """
    def __init__(self, x, n, q, N=None):
        self.x = x
        self.n = n
        self.q = q
        self._setup(N)
        self.prefac = 1
        self.postfac = 1

    def _setup(self, N):
        """Internal function to validate x and n, set N and _y, and compute
        coefficients :math:`u_m`, and XXXXXXXXXXX
        """
        import sympy
        from sympy.simplify.fu import TR8
        Nn = len(sympy.n)
        if Nn < 1 or not all(isinstance(sympy.n[i], int) and sympy.n[i]>=0
                                for i in range(Nn)):
            raise ValueError("n must be a nonempty sequence of nonnegative integers")
        x = sympy.symbols('x')
        y = sympy.symbols(' '.join('y{}'.format(i) for i in range(Nn)))
        sin_coeff, cos_coeff = [], []
        for i in range(Nn):
            jni = sympy.expand_func(sympy.jn(sympy.n[i], x * y[i]))
            sin_coeff.append(jni.coeff(sympy.sin(x * y[i])))
            cos_coeff.append(jni.coeff(sympy.cos(x * y[i])))

    def __call__(self, F, y, extrap=True):
        """Evaluate the integral

        Parameters
        ----------
        y : float, array_like
            output arguments, a list of :math:`y_i` arrays. If only one array
            is provided it will be used for each argument

        Returns
        -------
        G : float, array_like
            output function as an :math:`n`-dimensional array
        """

        # NOTE: something I wrote on the blackboard
        # interpolate before applying tilts
        # interpolate
        # apply tilts

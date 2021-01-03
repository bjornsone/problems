import math
import numpy as np


def _make_np(x):
    """If necessary, it converts to a 1d numpy array of length 2"""
    if isinstance(x, np.ndarray):
        return x
    else:
        return np.array(x)


def mag(p):
    """Returns the scalar magnitude of the given vector"""
    p = _make_np(p)
    return math.sqrt(p.dot(p))


def normed(p):
    """Returns the vector normalized to have magnitude of 1"""
    p = _make_np(p)
    return p/mag(p)


def rotated_90(p, is_clockwise=False):
    """Returns the 2D vector rotated by 90 degrees."""
    p = _make_np(p)
    if is_clockwise:
        return np.array([p[1], -p[0]])
    else:
        return np.array([-p[1], p[0]])


def project(v, p, factor=1.0):
    """Returns the projection of a rectangle of size v in the direction of p"""
    v, p = _make_np(v), _make_np(p)
    scale = sum(abs(v*p)) / p.dot(p) * factor
    return p * scale

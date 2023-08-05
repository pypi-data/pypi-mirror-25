import numpy as np

from .oneeurofilter import OneEuroFilter

__all__ = [
    'OneEuroFilter',
    'consecutive',
    'wrap_angles',
]


def consecutive(a, stepsize=1):
    """Returns the consecutive values in an array.

    >>> consecutive([1, 2, 4, 6, 7, 8])
    [array([1, 2]), array([4]), array([6, 7, 8])]
    """
    return np.split(a, np.where(np.diff(a) != stepsize)[0]+1)


def wrap_angles(a):
    """Wrap an array of angles to the interval [-pi, pi).
    """
    return (a + np.pi) % (2 * np.pi) - np.pi

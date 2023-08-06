#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 10:54:55 2017

@author: meikangfu
"""
import numpy as np
from .utils import _assert_compatible, remove_padding

def compare_mse(im1, im2, padding=0):
    """Compute the mean-squared error between two images.
    Parameters
    ----------
    im1 : ndarray
        The reference image.
    im2 : ndarray
        The reference image.
    Returns
    -------
    mse : float
        The mean-squared error (MSE) metric.
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Mean_squared_error
    """
    _assert_compatible(im1, im2)
    im1 = im1.astype(np.float32)
    im2 = im2.astype(np.float32)
    im1 = remove_padding(im1, padding)
    im2 = remove_padding(im2, padding)
    return np.mean(np.square(im1 - im2), dtype=np.float64)

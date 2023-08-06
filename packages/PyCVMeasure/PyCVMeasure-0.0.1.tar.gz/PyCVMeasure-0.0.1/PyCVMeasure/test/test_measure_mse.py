#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 11:19:06 2017

@author: meikangfu
"""
from PyCVMeasure.mse import compare_mse
from skimage import io
from scipy import misc
import pytest

def test_mse():
    hr = io.imread('img/Set5_HR.png')
    lr = io.imread('img/Set5_LR.png')
    with pytest.raises(ValueError):
        compare_mse(hr, lr)
    h, w, _ = lr.shape
    bicubic = misc.imresize(lr, (h*2, w*2), interp='bicubic')
    assert compare_mse(bicubic, hr)
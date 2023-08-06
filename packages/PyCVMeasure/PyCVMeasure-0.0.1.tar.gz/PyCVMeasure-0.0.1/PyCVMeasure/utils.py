#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 10:59:21 2017

@author: meikangfu
"""

import numpy as np

def remove_padding(im, padding):
    if padding == 0:
        return im
    h,w = im.shape
    return im[padding:h-padding,padding:w-padding]

def _assert_compatible(im1, im2):
    if not im1.dtype == im2.dtype:
        raise ValueError('Input images must have the same dtype.')
    if not im1.shape == im2.shape:
        raise ValueError('Input images must have the same shape.')
    return

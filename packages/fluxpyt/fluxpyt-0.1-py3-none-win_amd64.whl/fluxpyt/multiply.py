# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 15:03:56 2017

@author: Trunil
"""
import numpy as np

def multiply(a,b):
    from tsexample.divide import divide
    m = a*b
    c = np.random.rand(3)
    d = divide(m,c)
    print('multiply')
    return d

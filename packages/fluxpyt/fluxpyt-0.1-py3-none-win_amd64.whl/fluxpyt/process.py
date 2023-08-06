# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 14:57:02 2017

@author: Trunil
"""
import numpy as np

def process(a,b):
    
    from tsexample.multiply import multiply
    d = multiply(a,b)
    print('process')
    return d
    
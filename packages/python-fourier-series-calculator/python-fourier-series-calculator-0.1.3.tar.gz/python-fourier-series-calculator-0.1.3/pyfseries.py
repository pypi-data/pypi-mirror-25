# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 20:01:32 2017

@author: Joao Marcos Costa
"""


import numpy as np
from scipy import integrate

def _cos(x,func,n_,w_):
	return func(x)*np.cos(x*n_*w_)
	


	
def _sin(x,func,n_,w_):
	return func(x)*np.sin(x*n_*w_)
	
def an_bn(func,T0,n=10):
	bn=np.zeros(n)
	W = 2*np.pi/T0
	an=np.zeros(n)

	for i in range(n):
		an[i]=(2/T0)*(integrate.quad(_cos,0,T0,args=(func,i,W))[0])
		bn[i]=(2/T0)*(integrate.quad(_sin,0,T0,args=(func,i,W))[0])

	return an,bn

def rebuild(an_coefs,bn_coefs,T,x):
	w0 = 2*np.pi/T
	N = len(an_coefs)
	f_sum = 0
	for n in range(N):
		f_sum += an_coefs[n]*np.cos(x*n*w0)
		f_sum += bn_coefs[n]*np.sin(x*n*w0)
	return f_sum
	





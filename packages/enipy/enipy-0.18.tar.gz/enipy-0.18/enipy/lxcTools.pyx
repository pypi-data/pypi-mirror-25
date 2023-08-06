# cython: boundscheck=False
# cython: cdivision=True

cimport numpy as cnp
import numpy as np

def xcorr( float[:,:] x, float[:,:] y, float tau, float[:] trange, float dtmin=0.001 ):
	"""computes the cross correlation of x and y at lag tau, where 
	x and y are the waveshapes stored in a datafile, which means they 
	are arrays of time, amplitude pairs.
	
	Since the waveshapes are not sampled at equal intervals, this does 
	linear interpolation to improve the correlation estimation
	
	Note, this needs to be shoved over to cython asap
	"""
	
	cdef unsigned int N, i, j
	cdef double xc
	cdef float xv, xt, yv, yt, m
	
	#these numbers will contain a running sum of the correlation
	N  = 0	#the number of terms in the sum
	xc = 0
	
	#sample x, interpolate y
	j = 0
	for i in range( x.shape[0] ):
		
		#are we inside the timerange?
		xt = x[i,0]
		if xt < trange[0]:
			continue
		if xt > trange[1]:
			#we've left it, and there's no chance of coming back into it
			break
		
		xv = x[i,1]
		
		#find the first value of yt-tau larger than xt
		#note, we don't reset j, because xt is always increasing
		while y[j,0]+tau < xt:
			j += 1
			#catch edgecase
			if j >= y.shape[0]:
				break
		#catch end edgecase again
		if j >= y.shape[0]:
			break
		#catch the beginning edgecase
		if j == 0:
			continue
		#too far away breaks
		if y[j,0]+tau-xt > dtmin:
			continue
		if xt-y[j-1,0]+tau > dtmin:
			continue
			
		#y[j,0] is the first sample > xt, so that means y[j-1,0] is < xt
		#we will linearly interpolate to get the value at xt
		#calculate the slope of the line
		m  = (y[j,1]-y[j-1,1])/(y[j,0]-y[j-1,0])
		#calculate the expected value
		yv = m*(xt - tau-y[j-1,0]) + y[j,1]
		
		xc += yv*xv
		N  += 1
			
	#sample y, interpolate x
	if N == 0:
		return 0
	return xc/N

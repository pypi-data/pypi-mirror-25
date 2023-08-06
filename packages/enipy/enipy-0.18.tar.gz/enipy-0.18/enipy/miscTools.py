#!/usr/bin/python
########################################################################
# miscTools
# Various functions which are used in multiple places.  Generally this 
# all functions in this library are imported by the other tools
#
# Copyright (c) 2017 Earth Networks, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import time, calendar

########################################################################
# Useful Fundamental Constants
R_EARTH = 6371000.		#meters
C       = 299792458. 	#m/s
PI      = np.pi

########################################################################
# Distance Functions

def spherical_distance( pt1, pt2, ):
	"""Calculates the distance between two points on a sphere.  Will 
	work on vectors of positions as well.
	
	This is the well known haversine equation.
	"""
	#math imports
	from numpy import cos, sin, arctan2, pi, sqrt
	
	#copy and convert to radians
	lat1 = pt1[0]*pi/180
	lat2 = pt2[0]*pi/180
	lon1 = pt1[1]*pi/180
	lon2 = pt2[1]*pi/180
	dlat = lat1-lat2
	dlon = lon1-lon2
	
	a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
	rng = R_EARTH * 2 * arctan2( sqrt(a), sqrt( 1-a ) )
	
	return rng

def spherical_bearing( pt1, pt2 ):
	"""Calculates the forward azimuth between pt1 and pt2.  You can 
	get the back azimuth by calling on pt2, pt1.
	"""
	#mat imports
	from numpy import cos, sin, arctan2, pi

	#copy and convert to radians
	lat1 = pt1[0]*pi/180
	lat2 = pt2[0]*pi/180
	lon1 = pt1[1]*pi/180
	lon2 = pt2[1]*pi/180	
	
	x = sin(lon2-lon1)*cos(lat2)
	y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(lon2-lon1)
	return np.arctan2( x, y )

def spherical_intersection( pt1, brg1, pt2, brg2 ):
	"""Calculates the intersection point between two lat-lon points and 
	their forward bearings
	This one is a little more complex
	
	There are some edge cases with this that I'm not testing, there are 
	certain points/bearings which will never intersect.
	"""
	###
	# gonna need these.  Maybe they've already been imported, but 
	# it won't hurt to do it again
	from numpy import arcsin, arctan2, arccos, sin, cos, pi, sqrt
	
	#convert to radians
	lat1 = pt1[0]*pi/180
	lat2 = pt2[0]*pi/180
	lon1 = pt1[1]*pi/180
	lon2 = pt2[1]*pi/180
	
	dlat = lat1-lat2
	dlon = lon1-lon2

	#angular distance between pt1 and pt2
	a12 = 2*arcsin( sqrt( 
		sin( dlat/2 )**2 +\
		cos(lat1)*cos(lat2)*sin(dlon/2 )**2 
		) )
	
	#bearings
	brg12 = spherical_bearing(pt1,pt2)
	brg21 = spherical_bearing(pt2,pt1)
	
	#angles
	alpha1 = brg1-brg12
	alpha2 = brg21-brg2
	alpha3 = arccos( 
				-cos(alpha1)*cos(alpha2) +\
				 sin(alpha1)*sin(alpha2)*cos(a12) )
	
	#angular distance between pt1 and the intersection
	a13 = arctan2( 
			sin(a12)*sin(alpha1)*sin(alpha2), 
			cos(alpha2)+cos(alpha1)*cos(alpha3)
			)
	
	#now getting the lat-lon is 'easy'
	
	lat3 = arcsin( 
			sin(lat1)*cos(a13)+\
			cos(lat1)*sin(a13)*cos(brg1) )
	lon3 = lon1 +\
			arctan2( sin(brg1)*sin(a13)*cos(lat1), 
					 cos(a13)-sin(lat1)*sin(lat3) )
	
	#convert to lat-lon, and return
	return lat3*180/pi, lon3*180/pi

def rngbrg2latlon( rng, brg, pt ):
	"""converts range and bearing from a lat-lon point to a lat-lon point
	"""
	###
	# gonna need these.  Maybe they've already been imported, but 
	# it won't hurt to do it again
	from numpy import arcsin, arctan2, sin, cos, pi
	
	lat1 = pt[0]*pi/180
	lon1 = pt[1]*pi/180
	
	d = rng/R_EARTH
	
	lat2 = arcsin( sin(lat1)*cos(d) + cos(lat1)*sin(d)*cos(brg) )
	lon2 = lon1 + arctan2( sin(brg)*sin(d)*cos(lat1), cos(d)-sin(lat1)*sin(lat2) )
	
	#lat and lon should be returned in degrees
	return lat2*180/pi, lon2*180/pi

def latlon2rngbrg( pt1, pt2):
	"""Calculates the range and bearing between 2 lat-lon points
	"""	
	
	rng = spherical_distance( pt1, pt2 )
	brg = spherical_bearing( pt1, pt2 )
	
	return rng, brg

########################################################################
# Polygon Functions

def inside_polygon( pt, poly ):
	"""tests if pt is inside poly
	This is done in catesian lat-lon coordinates, which is a bit odd
	"""
	
	#these are subfunctions for the inside polygon test
	def onSegment( p, q, r ):
		"""is p on segment rq
		"""
		if  ( q[0] <= max(p[0],r[0]) ) and \
			( q[0] >= min(p[0],r[0]) ) and \
			( q[1] <= max(p[1],r[1]) ) and \
			( q[1] >= min(p[1],r[1]) ) :
				return True
		return False

	def orientation( p, q, r ):
		v = (q[1]-p[1]) * (r[0]-q[0]) -\
			(q[0]-p[0]) * (r[1]-q[1])
		
		if v==0:
			return 0
		elif v>0:
			return 1
		else:
			return -1

	def doIntersect( p1, q1, p2, q2 ):
		"""Do line segments p1q1 and p2q2 intersect?
		"""
		o1 = orientation(p1,q1,p2)
		o2 = orientation(p1,q1,q2)
		o3 = orientation(p2,q2,p1)
		o4 = orientation(p2,q2,q1)
		
		if (o1!=o2) and (o3!=o4):
			return True
		
		if (o1==0) and onSegment(p1,p2,q1): return True
		if (o2==0) and onSegment(p1,q2,q1): return True
		if (o3==0) and onSegment(p2,p1,q2): return True
		if (o4==0) and onSegment(p2,q1,q2): return True
		
		#else
		return False

	
	if len(poly) < 3:
		#there's not enough vertices in the polygon for the point to be 
		#inside of
		return False
	
	ptInf = pt[0], 720.	#that's outside the planet
	
	i = 0
	count = 0
	while i < len(poly):
		j = (i+1)%(len(poly))
	
		if doIntersect( poly[i], poly[j], pt, ptInf ):
			if orientation(poly[i], pt, poly[j])==0:
				return onSegment( poly[i], pt, poly[j] )
			
			count += 1
		
		i += 1
	
	if count%2==0:
		return False
	else:
		return True

def polygon_union( poly1, poly2 ):
	
	poly = []
	
	###
	# start on poly1
	i = 0
	#step one, make sure we're not inside poly2
	while inside_polygon( poly1[i], poly2 ):
		i += 1
		if i > len(poly1):
			return poly1
	#now append poly1's points
	while not inside_polygon( poly1[i], poly2 ):
		if inside_polygon( poly1[i], poly2 ):
			break
		poly.append(poly1[i])
		i+=1
	#i is now inside poly2, so append poly2's points
	#step 1: find the closest point in poly2 to poly[-1]
	j = 0
	dMin = R_EARTH
	j0 = 0
	while j<len(poly2):
		d = spherical_distance( poly2[j], poly[-1] ) 
		if d < dMin:
			dMin = d
			j0 = j
		j += 1
	#reorder poly2 (this won't work if poly2 is an np.ndarray)
	poly2 = poly2[j0:] + poly2[:j0]
	#loop over poly2
	j = 0
	while inside_polygon( poly2[j], poly1 ):
		j += 1
		if j > len(poly2):
			#the polygons must not overlap, we should have causght this already
			return poly1
	while not inside_polygon( poly2[j], poly1 ):
		poly.append( poly2[j] )
		j += 1
		
	#switch back to poly1
	#get outside of poly2
	while inside_polygon( poly1[i], poly2 ):
		i += 1
		if i >=len(poly1):
			return poly
	#now append the last of poly1's points
	while not inside_polygon( poly1[i], poly2 ):
		poly.append(poly1[i])
		i+=1
		if i>=len(poly1):
			return poly
	
	return poly

########################################################################
# Time Functions
def timeStamp2time( S ):
	###
	# converts a timeStamp into a time in seconds
	# this would be simpler if we didn't want the fractional part 
	# in ns
	
	# strip all non-numbers from the time
	s = ''
	for i in range(len(S)):
		if S[i] in '0123456789':
			s += S[i]
	S = s
	# now we're going to rashly assume that the data format is:
	# YmdHMSF where F is the fractional part
	# that means it is: 14+F characters long
	nano = S[14:]
	sec  = S[:14]
	# pad things with 0's until the length is right
	while len(nano) < 9:
		nano += '0'
	while len(sec) < 14:
		sec += '0'
	nano = int(nano)
	sec  = calendar.timegm( time.strptime( S[:14], '%Y%m%d%H%M%S' ) )
	
	
	return sec+nano/1e9, sec, nano
	
def time2timeStamp( t ):
	S = time.strftime( '%Y-%m-%dT%H:%M:%S', time.gmtime( t ) )
	#that gets us to the second, we still have to deal with the fractional part
	S += ('%0.9f'%np.modf( t )[0])[1:]
	
	return S
	

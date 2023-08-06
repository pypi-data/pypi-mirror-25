#!/usr/bin/python
########################################################################
# visTools
# Tools for making visualizations of Earth Networks data
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

# we need the time library for all sorts of reasons
import time
# array math
import numpy as np
# plotting libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.basemap import Basemap
# used for pulling map tiles from Openstreetmap server
import urllib2, os, StringIO, math
from PIL import Image

# the common utilities
from miscTools import *

DEBUGGING = True

########################################################################
# Colors
colorDict = {	'red': ( 	(0.00, 0.2, 0.2),
							(0.15, 0.2, 0.2),
							(0.50, 1.0, 1.0),
							(0.85, 1.0, 1.0),
							(1.00, 0.7, 0.7) ),
				'green':(	(0.00, 0.2, 0.2),
							(0.15, 0.5, 0.5),
							(0.50, 1.0, 1.0),
							(0.85, 0.1, 0.1),
							(1.00, 0.0, 0.0) ),
				'blue':(	(0.00, 0.7, 0.7),
							(0.15, 1.0, 1.0),
							(0.50, 1.0, 1.0),
							(0.85, 0.0, 0.0),
							(1.00, 0.0, 0.0) ) }

cmBWR = colors.LinearSegmentedColormap('bwr',colorDict,256)

colorDict = {	'red': 	( 	(0, .3, .3 ),
							(1, .3, .3 ) ),
				'blue':	(	(0, .3, .3 ), 
							(1, .3, .3 ) ),
				'green':(	(0, .3, .3 ),
							(1, .3, .3 ) ),
				'alpha':( 	(0,  0,  0 ), 
							(1,  1,  1) ) }

cmTransGray = colors.LinearSegmentedColormap('transgray',colorDict,256)

colorDict = {	'red': ( 	(0.00, 0.3, 0.3),
							(0.15, 0.0, 0.0),
							(0.20, 0.0, 0.0),
							(0.50, 0.0, 0.0),
							(0.70, 1.0, 1.0),
							(0.90, 1.0, 1.0),
							(1.00, 0.7, 0.7) ),
				'green':(	(0.00, 0.0, 0.0),
							(0.15, 0.0, 0.0),
							(0.25, 0.3, 0.3),
							(0.45, 1.0, 1.0),
							(0.70, 0.9, 0.9),
							(0.90, 0.0, 0.0),
							(1.00, 0.0, 0.0) ),
				'blue':(	(0.00, 0.5, 0.5),
							(0.20, 1.0, 1.0),
							(0.45, 1.0, 1.0),
							(0.50, 0.1, 0.1),
							(0.70, 0.0, 0.0),
							(0.90, 0.0, 0.0),
							(1.00, 0.0, 0.0) ),
				'alpha':(	(0.00, 0.0, 0.0),
							(1.00, 1.0, 1.0) ) }
cmTransJet   = colors.LinearSegmentedColormap('transjet',colorDict,256)

colorDict = {	'red': ( 	(0.00, 0.3, 0.3),
							(0.15, 0.0, 0.0),
							(0.20, 0.0, 0.0),
							(0.50, 0.0, 0.0),
							(0.70, 1.0, 1.0),
							(0.90, 1.0, 1.0),
							(1.00, 0.7, 0.7) ),
				'green':(	(0.00, 0.0, 0.0),
							(0.15, 0.0, 0.0),
							(0.25, 0.3, 0.3),
							(0.45, 1.0, 1.0),
							(0.70, 0.9, 0.9),
							(0.90, 0.0, 0.0),
							(1.00, 0.0, 0.0) ),
				'blue':(	(0.00, 0.5, 0.5),
							(0.20, 1.0, 1.0),
							(0.45, 1.0, 1.0),
							(0.50, 0.1, 0.1),
							(0.70, 0.0, 0.0),
							(0.90, 0.0, 0.0),
							(1.00, 0.0, 0.0) ),
				'alpha':(	(0.00, 0.0, 0.0),
							(0.01, 1.0, 1.0),
							(1.00, 1.0, 1.0)) }
cmTransJet2   = colors.LinearSegmentedColormap('transjet',colorDict,17)

#colorblind safe set of 12 color Jet + transparent
colorDict = {	'red':(		(0.00, 0.00, 0.00),
							(0.07, 0.00, 0.47),
							(0.15, 0.47, 0.25),
							(0.23, 0.25, 0.25),
							(0.30, 0.25, 0.28),
							(0.38, 0.28, 0.33),
							(0.46, 0.33, 0.39),
							(0.54, 0.39, 0.50),
							(0.61, 0.50, 0.71),
							(0.69, 0.71, 0.85),
							(0.76, 0.85, 0.90),
							(0.85, 0.90, 0.90),
							(0.92, 0.90, 0.85),
							(1.00, 0.85, 0.85) ),
				'green':(	(0.00, 0.00, 0.00),
							(0.07, 0.00, 0.11),
							(0.15, 0.11, 0.23),
							(0.23, 0.23, 0.39),
							(0.30, 0.39, 0.54),
							(0.38, 0.54, 0.63),
							(0.46, 0.63, 0.67),
							(0.54, 0.67, 0.72),
							(0.61, 0.72, 0.74),
							(0.69, 0.74, 0.68),
							(0.76, 0.68, 0.55),
							(0.85, 0.55, 0.39),
							(0.92, 0.39, 0.13),
							(1.00, 0.13, 0.13) ),
				'blue':(	(0.00, 0.00, 0.00),
							(0.07, 0.00, 0.50),
							(0.15, 0.50, 0.57),
							(0.23, 0.57, 0.69),
							(0.30, 0.69, 0.75),
							(0.38, 0.75, 0.69),
							(0.46, 0.69, 0.60),
							(0.54, 0.60, 0.44),
							(0.61, 0.44, 0.30),
							(0.69, 0.30, 0.23),
							(0.76, 0.23, 0.20),
							(0.85, 0.20, 0.17),
							(0.92, 0.17, 0.12),
							(1.00, 0.12, 0.12) ),
				'alpha':(	(0.00, 0.00, 0.00),
							(0.06, 0.00, 1.00),
							(1.00, 1.00, 1.00) ) }
cmTransCBJet   = colors.LinearSegmentedColormap('transjet',colorDict,13)


########################################################################
# Functions

######
# Functions for making maps
def make_map( bbox, ax=None, zoom=None, **kwargs ):
	"""
	goes through all the typical generation steps to make a map with 
	a background image for the given bbox.  
	
	This is really just a wrapper around mpl.Basemap, and kwargs are 
	passed onto mpl.Basemap
	"""
	if ax == None:
		ax = plt.subplot(111)
	
	
	if zoom == None:
		#we need to guess it
		zoom = int(bbox[0][1] - bbox[0][0])/15
	
	###
	# download the map tiles, noting that the image bbox will not 
	# be the same as input bbox
	mapImage, imageBbox = get_image_cluster(bbox, zoom)

	###	
	# create the basemap instance
	# we need to use the merc projection for the image tiles and the 
	# basemap to match up
	figMap = Basemap(
		llcrnrlat=imageBbox[0][0], llcrnrlon=imageBbox[1][0],
		urcrnrlat=imageBbox[0][1], urcrnrlon=imageBbox[1][1],
		projection='merc', ax=ax, **kwargs
		)

	###
	# place the mage image onto a basemap instance
	figMap.imshow(mapImage, interpolation='lanczos', origin='upper')

	###
	# update the map's limits to match the input bbox
	# annoyingly, this is not documented in the Basemap utilities
	# so, we have to do this through the figAx instead
	xmin, ymin = figMap( bbox[1][0], bbox[0][0] )
	xmax, ymax = figMap( bbox[1][1], bbox[0][1] )
	ax.set_xlim( xmin, xmax )
	ax.set_ylim( ymin, ymax )
	
	return figMap, ax

def draw_map_grid( figMap, meridians=None, parallels=None, spacing=None, **kwargs):
	"""
	Basemap has a built in method for drawing parallels and meridians, 
	but it doesn't work very well if you ever plan to change the limits 
	of the plot.  So, I've re-implemented it.
	
	kwargs are passed onto the plot method
	nothing is returned
	"""

	#set some default kwargs, if they weren't already set
	if 'color' not in kwargs:
		kwargs['color'] = (.5,.5,.5)
	if 'ls' not in kwargs:
		kwargs['ls'] = '-'
	if 'alpha' not in kwargs:
		kwargs['alpha'] = 0.3
	

	# first generate the bbox
	bbox     = [ [figMap.latmin, figMap.latmax], [figMap.lonmin, figMap.lonmax] ]
	# and get the axis
	figAx    = figMap.ax
	
	# get the current limits
	xlim = figAx.get_xlim()
	ylim = figAx.get_ylim()
	
	###
	# step 1, we need to decide where to plot the meridians and parallels
	if  (meridians is not None) and (parallels is None):
		if spacing is None:
			spacing = meridians[1]-meridians[0]
		#calculate parallels
		pmin = (figMap.latmin//spacing+1)*spacing
		parallels = np.arange( pmin, figMap.latmax, spacing )
	elif (meridians is None) and (parallels is not None):
		if spacing is None:
			spacing = parallels[1]-parallels[0]
		#calculate meridians
		mmin = (figMap.lonmin//spacing+1)*spacing
		meridians = np.arange( mmin, figMap.lonmax, spacing )			
	else:
		if spacing is None:
			spacing = [ .5, 1, 2, 5, 10, 20, 60 ]
			#both are none, we have some work to do
			dlat = figMap.latmax-figMap.latmin
			dlon = figMap.lonmax-figMap.lonmin
			#we just need to test the shorter of these two
			d = min( [dlat, dlon] )
			i = 0
			N = dlat/spacing[i]
			while N >= 5:
				i += 1
				N = d/spacing[i]
			#collapse the possible spacings
			spacing = spacing[i]
		#calculate parallels
		pmin = (figMap.latmin//spacing+1)*spacing
		parallels = np.arange( pmin, figMap.latmax, spacing )			
		#calculate meridians
		mmin = (figMap.lonmin//spacing+1)*spacing
		meridians = np.arange( mmin, figMap.lonmax, spacing )		

	###
	# now that parallels and meridians are both enumerated, draw them
	yticks = []
	ytick_labels = []
	xticks = []
	xtick_labels = []
	for p in parallels:
		#these are lines of x parallel, so they have labels on the 
		#yaxis
		lats = np.zeros( 20 )+p
		lons = np.linspace( figMap.lonmin, figMap.lonmax, 20 )
		x, y = figMap( lons, lats )
		yticks.append( y[0] )
		ytick_labels.append( '%1.1f'%p )
		# ytick_labels.append( repr(p) )
		#plot the line
		figMap.plot( x, y, **kwargs )
	for m in meridians:
		#these are lines of x parallel, so they have labels on the 
		#yaxis
		lons = np.zeros( 20 )+m
		lats = np.linspace( figMap.latmin, figMap.latmax, 20 )
		x, y = figMap( lons, lats )
		xticks.append( x[0] )
		xtick_labels.append( '%1.1f'%m )
		#~ xtick_labels.append( repr(m) )
		#plot the line
		figMap.plot( x, y, **kwargs )
	
	###
	# set the ticks and labels
	figAx.set_xticks( xticks )
	figAx.set_xticklabels( xtick_labels )
	figAx.set_xlim( xlim )
	figAx.set_yticks( yticks )
	figAx.set_yticklabels( ytick_labels )
	figAx.set_ylim( ylim )
		

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  """
  http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
  This returns the NW-corner of the square. 
  Use the function with xtile+1 and/or ytile+1 to get the other corners. 
  With xtile+0.5 & ytile+0.5 it will return the center of the tile.
  """
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def get_image_cluster( bbox, zoom):
	###
	# Modified off some code I pulled from stack exchange.  This 
	# should be updated a bit, and it would be nice if any map tile 
	# server was supported.
	
	locurl = r"./.maptiles/{0}/{1}/{2}.png"
	smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
	
	# the map coordinates are not in lat, lon.  So we need to convert here
	xmin, ymax = deg2num(bbox[0][0], bbox[1][0], zoom)
	xmax, ymin = deg2num(bbox[0][1], bbox[1][1], zoom)
	print xmin, xmax, ymin, ymax

	bbox_ul = num2deg(xmin, ymin, zoom)
	bbox_ll = num2deg(xmin, ymax + 1, zoom)
	print bbox_ul, bbox_ll

	bbox_ur = num2deg(xmax + 1, ymin, zoom)
	bbox_lr = num2deg(xmax + 1, ymax +1, zoom)
	print bbox_ur, bbox_lr

	print ((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1)
	Cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) )
	for xtile in range(xmin, xmax+1):
		for ytile in range(ymin,  ymax+1):
			try:
				imgurl=smurl.format(zoom, xtile, ytile)
				imgloc=locurl.format(zoom, xtile, ytile)
				if os.path.exists( imgloc ):
					if DEBUGGING:
						print("Opening: " + imgloc)
					# we have a local copy
					f = open( imgloc, 'r' )
					imgstr = f.read()
					f.close()			
				else:
					if DEBUGGING:
						print("Opening: " + imgurl)
					imgstr = urllib2.urlopen(imgurl).read()
					###
					# make the local directory
					dirS = os.path.split( imgloc )[0]
					if not os.path.exists( dirS ):
						if DEBUGGING:
							print('making directory'+dirS)
						os.makedirs( dirS )
					if DEBUGGING:
						print("Writing: " + imgloc)
					# write the local copy
					f = open( imgloc, 'w' )
					f.write( imgstr )
					f.close()
				
				#we go through all that trouble of reading in the data, 
				#then use StringIO to treat the string like a file, hehe
				tile = Image.open(StringIO.StringIO(imgstr))
				Cluster.paste(tile, box=((xtile-xmin)*255 ,  (ytile-ymin)*255))
			except: 
				print("Couldn't download image")
				tile = None

	return Cluster, [[bbox_ll[0], bbox_ur[0]], [bbox_ll[1], bbox_ur[1]] ]
	
######
# Functions for Lightning

def pulse_density( lats, lons, bbox, pixelSize=0.1 ):
	
	#generate the output arrays
	Nx = (bbox[1][1]-bbox[1][0])/pixelSize
	Ny = (bbox[0][1]-bbox[0][0])/pixelSize
	
	# we'll just do this with histogram2d
	output = np.histogram2d( lons, lats, range=[bbox[1],bbox[0]], bins=[Nx, Ny] )
	
	return output


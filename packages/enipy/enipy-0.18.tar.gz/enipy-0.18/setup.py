from setuptools import setup,find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_descriptionFile = f.read()

with open(path.join(here, 'LICENSE.txt'), encoding='utf-8') as f:
    licenseFile = f.read() 
import numpy
  
ext = Extension("enipy.lxcTools", ["enipy/lxcTools.pyx"], 
    include_dirs = [numpy.get_include()])
  
setup( 
	name='enipy', 
	version='0.18',
	packages=['enipy',],
	ext_modules=[ext],
        #install_requires=['cython','numpy'],
        author = 'Earth Networks',
        author_email = 'support@earthnetworks.com',
        url = 'https://bitbucket.org/earthnetworksrd/enipy',
	license=licenseFile,
	long_description=long_descriptionFile,
	cmdclass = {'build_ext': build_ext}	
	)

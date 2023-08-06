#!python
#-- setup.py -- smash

#----------------------------------------------------------------------#

from setuptools import setup
from smash.setup.arguments import kwargs
import os

with open( os.path.join( os.path.dirname( __file__ ), 'DESCRIPTION.rst' ) ) as r_file :
    long_description = r_file.read()

setup( **kwargs, long_description=long_description )


#----------------------------------------------------------------------#

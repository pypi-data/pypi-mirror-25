#-- smash.core.env

"""
"""

from powertools import AutoLogger
log = AutoLogger()

import sys
from powertools import classproperty
from powertools import export
from powertools import assertion

from contextlib import contextmanager

#----------------------------------------------------------------------#
@export
class Platform:
    ''' keep track of differences between platforms '''

    @classproperty
    def match(cls) -> bool:
        '''check the type of the host platform'''

        raise NotImplementedError


#----------------------------------------------------------------------#
@export
class Win32(Platform):
    ''' windows '''

    @classproperty
    def match( cls ) :
        return sys.platform == 'win32'

    def __str__(self):
        return 'Win32'


#----------------------------------------------------------------------#
@export
class Linux(Platform):
    ''' everything else '''

    @classproperty
    def match( cls ) :
        return sys.platform in ('linux', 'linux2')

    def __str__( self ) :
        return 'Linux'


#----------------------------------------------------------------------#
@export
class Mac(Platform):
    ''' another type of linux '''

    @classproperty
    def match( cls ) :
        return False

    def __str__( self ) :
        return 'Mac'


#----------------------------------------------------------------------#

class PlatformError(Exception):
    '''unsupported or unknown platform'''

@export
def match():
    if Win32.match:
        return Win32
    elif Linux.match:
        return Linux
    elif Mac.match:
        return Mac
    else:
        raise PlatformError('unknown platform')

def trycall(obj, args, kwargs):
    try:
        return obj(*args, **kwargs)
    except TypeError:
        return obj


def switch(
        case_win = NotImplemented,
        case_nix = NotImplemented,
        case_mac = NotImplemented,
        *args, **kwargs ):
    ''' switch between 3 options depending on the current platform
        return the value of `case_*`,
        first, attempt to execute it as a function of args and kwargs
    '''
    case        = NotImplemented
    platform    = match()
    if platform   == Win32: case = case_win
    elif platform == Linux: case = case_nix
    elif platform == Mac:   case = case_mac

    with assertion(PlatformError(f'missing implementation {str(platform)}')):
        assert case is not NotImplemented

    return trycall( case, args, kwargs )


class MissingKeyError(Exception):
    ''' dictionary did not contain a key for the requested platform '''

def choose(pdict):
    ''' choose a value out of a dict keyed by str(Platform())
        __inherit__:
          - Win32: ${HOME}/__win__.yml
          - Linux: ${HOME}/__nix__.yml
          - Linux: ${HOME}/__nix__.yml
    '''
    try:
        key = str( match()() )
        return pdict[key]
    except KeyError as e:
        raise MissingKeyError(key)

#----------------------------------------------------------------------#

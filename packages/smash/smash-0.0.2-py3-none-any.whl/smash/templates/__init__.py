#-- smash.core.constants

"""
global constants
"""

from pathlib import Path

#----------------------------------------------------------------------#

TEMPLATES_ROOT      = Path( __file__ ).parents[0]

ROOT_YAMLISP        = '__root__.yml'
ENV_YAMLISP         = '__env__.yml'
PKG_YAMLISP         = '__pkg__.yml'

STOP_FILE           = TEMPLATES_ROOT / '__stop__'
SMASH_PY            = TEMPLATES_ROOT / 'smash.py'
SMASH_SPEC          = TEMPLATES_ROOT / 'smash.spec'

INSTANCE_CONFIG     = TEMPLATES_ROOT / 'instance' / ROOT_YAMLISP
ENV_CONFIG          = TEMPLATES_ROOT / 'instance' / ENV_YAMLISP
PKG_CONFIG          = TEMPLATES_ROOT / 'instance' / PKG_YAMLISP

NIX_HOST            = TEMPLATES_ROOT / 'host-nix'
WIN_HOST            = TEMPLATES_ROOT / 'host-win'
NET                 = TEMPLATES_ROOT / 'net'
PYTHON              = TEMPLATES_ROOT / 'python'


#----------------------------------------------------------------------#

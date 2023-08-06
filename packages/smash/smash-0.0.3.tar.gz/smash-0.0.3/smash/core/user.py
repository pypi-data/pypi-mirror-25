#-- smash.core.user

"""
keep track of user-specific information, including authentication details
"""


import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print

from pathlib import Path

from powertools import export

#----------------------------------------------------------------------#

@export
class User:
    '''nothing here yet'''

    NotImplemented


#----------------------------------------------------------------------#

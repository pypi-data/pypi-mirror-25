#-- smash.boot.strap

"""
"""

from powertools import export
from powertools import AutoLogger
log = AutoLogger( )

################################
from pathlib import Path


#----------------------------------------------------------------------#

def create_instance(instance_root:Path):
    '''create '''

    yield
    #teardown


#----------------------------------------------------------------------#

def install_configsystem( install_root: Path, name:str, *, force=False ) :
    if install_root.exists( ) :
        # todo: make backup
        pass

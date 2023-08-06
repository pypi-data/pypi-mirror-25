#-- smash.boot.context_menus

"""
environment management
"""


from powertools import export
from powertools import AutoLogger
log = AutoLogger( )

################################
from pathlib import Path


#----------------------------------------------------------------------#

def register_script_to_context_menu( ) :
    # http://support.microsoft.com/kb/310516
    cmd_line = 'regedit.exe registerOne.reg'
    import os
    os.system( cmd_line )

#----------------------------------------------------------------------#



#----------------------------------------------------------------------#

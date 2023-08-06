#-- smash.pkg.__main__

'''
application entry point
'''

from powertools import export
from powertools import AutoLogger

log = AutoLogger()
from powertools import term

import os
import sys
import traceback
import argparse
import click

from pathlib import Path
from collections import namedtuple
from collections import deque

from ..core.env import ContextEnvironment
from ..core.env import InstanceEnvironment
from ..core.env import VirtualEnvironment

#----------------------------------------------------------------------#



##############################
@click.group()
@click.option( '--verbose', '-v', default=False, is_flag=True )
@click.option( '--simulation', '-S', default=False, is_flag=True )
@click.pass_context
def console( ctx, verbose, simulation ) :
    ''' basic utilities for managing smash instances on a host '''

    term.init_color()

    log.print( term.cyan( '\n~~~~~~~~~~~~~~~~~~~~ ' ), term.pink( 'SMASH' ), term.cyan( '.' ), term.pink( 'PKG' ) )
    log.print( 'SCRIPT:  ', __file__ )
    cwd = Path( os.getcwd() )
    log.print( 'WORKDIR: ', cwd )

    ### precreate context environment
    from ..core.env import ContextEnvironment
    context_env = ContextEnvironment( cwd )
    ctx.obj = namedtuple( 'Arguments', ['context', 'verbose', 'simulation'] )(
        context_env, verbose, simulation )


##############################
@console.command()
@click.argument( 'package_path' )
@click.pass_context
def install( ctx, package_path) :
    ''' install a package '''

    args = ctx.obj
    ### wild lands of unmanaged state
    with args.context as context :
        ### the wall that guards the lands of version control
        with InstanceEnvironment( parent=context ) as instance :
            ### virtual environments may use a different python version from instance
            with VirtualEnvironment( instance ) as interior :

                ...


    log.print( '\n', term.pink( '~~~~~~~~~~~~~~~~~~~~' ), term.cyan( ' DONE ' ), '...' )

#----------------------------------------------------------------------#

if __name__ == '__main__' :
    console()

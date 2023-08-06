#-- smash.__main__

'''
application entry point
'''

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

from powertools import term

from pathlib import Path
from collections import namedtuple

import os
import sys
import click

#----------------------------------------------------------------------#

class UnknownTemplateError( Exception ) :
    '''template_name argument was not found in the templates dictionary'''


##############################
@click.group()
@click.option( '--verbose', '-v',       default=False, is_flag=True )
@click.option( '--simulation', '-S',    default=False, is_flag=True )
@click.pass_context
def console( ctx , verbose, simulation ) :
    ''' basic utilities for managing smash instances on a host '''

    term.init_color()

    log.print( term.cyan( '\n~~~~~~~~~~~~~~~~~~~~ ' ), term.pink( 'SMASH'),term.cyan('.'), term.pink('BOOT' ) )
    log.print( 'SCRIPT:  ', __file__ )
    cwd = Path( os.getcwd() )
    log.print( 'WORKDIR: ', cwd )

    ### precreate context environment
    from ..core.env import ContextEnvironment
    context_env = ContextEnvironment( cwd )
    ctx.obj     = namedtuple('Arguments', ['context_env', 'verbose', 'simulation'])(
                                            context_env,   verbose,   simulation )


##############################
@console.command()
@click.argument( 'instance_name' )
@click.argument( 'template_name', default = 'smash' )
@click.pass_context
def create( ctx, instance_name:str, template_name:str ) :
    ''' create new instance root in target directory using a registered template '''
    from ..core.plugins import instance_templates
    try:
        parent_args     = ctx.obj
        template        = instance_templates[template_name]
        install_root    = parent_args.context_env.homepath.resolve() / instance_name

        ### template creates the instance
        instance        = template( install_root,
                                    simulation  = parent_args.simulation,
                                    parent      = parent_args.context_env
                                    ).instance

    except KeyError as e:
        raise UnknownTemplateError(e)

    log.print( '\n', term.pink( '~~~~~~~~~~~~~~~~~~~~' ), term.cyan(' DONE '), '...' )


##############################
@console.command()
def build() :
    ''' build executable distribution archive '''


##############################
@console.command()
def test() :
    ''' run deployment tests on an instance or an archive '''


##############################
@console.command()
def push() :
    ''' upload archive to deployment registry '''


##############################
@console.command()
def clone() :
    ''' pull an instance archive from the deployment registry and extract it to a new directory '''


##############################
if __name__ == '__main__' :
    console()


#----------------------------------------------------------------------#

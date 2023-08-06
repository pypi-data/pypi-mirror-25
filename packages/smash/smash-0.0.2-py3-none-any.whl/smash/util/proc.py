#-- smash.sys.tools

"""
call command-line utilities as subprocesses
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import psutil

from ..core.config import ConfigTree

from collections import OrderedDict

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    __all__.append( obj.__name__ )
    return obj


#----------------------------------------------------------------------#

SUBPROCESS_DELAY = 0.01
@export
def execute( command_string: str, env=None ) -> (int, list) :
    # command = shlex.split(command_string)
    proc = subprocess.Popen( command_string, env=env, shell=True )
    pid_shell = proc.pid

    # collect child pids so they can be stored for later termination
    pids_children = [process.pid for process in psutil.Process( pid_shell ).children( recursive=True )]

    time.sleep( SUBPROCESS_DELAY )
    proc.terminate( ) #terminate exterior shell
    proc.wait( )
    return pid_shell, pids_children

@export
def execute2( command: str, path: Path = None, env=None ) -> (int, list) :
    proc = subprocess.Popen(
        command,
        env=env,
        cwd=str( path ),
        shell=True
    )
    pid_shell = proc.pid

    ### collect child pids so they can be stored for later termination
    pids_children = [process.pid for process in psutil.Process( pid_shell ).children( recursive=True )]

    # todo: detect and report when command is not found, or exits with nonzero return

    time.sleep( SUBPROCESS_DELAY )
    proc.terminate() #terminate exterior shell
    proc.wait()
    return pid_shell



@export
def kill_all( pids: list ) :
    for pid in pids :
        os.kill( pid, signal.SIGTERM )


#----------------------------------------------------------------------#


# @export
# def load_configs(cwd:Path):
#
#     try :
#         configs = ConfigTree.from_path( cwd)
#     except FileNotFoundError as e :
#         configs = ConfigTree()
#     print("configs", configs)
#     return configs
#




# @export
# def build_subenv( configs:ConfigTree, pure_mode=False ):
#     if not pure_mode:
#         subenv = os.environ.copy( )
#     else:
#         subenv = OrderedDict()
#
#     try:
#         for (key, value) in configs.data['shell'].items():
#             subenv[key] = value
#     except KeyError as e:
#         pass
#
#     # ToDo: construct pythonpath
#     # ToDo: construct pythonhome
#     # ToDo: construct path
#
#
#     return subenv
#

#----------------------------------------------------------------------#

# ToDo: pooling of service ports
# How do I synchronize knowledge of the ports that processes distributed across hosts need?
# Need a cluster-level config layer

# @export
# def run_service_yaml( cwd: Path, verbose=False ) -> list :
#     children = None
#
#     return children


#----------------------------------------------------------------------#
#
# @export
# def run_cmd( subenv: dict, working_dir:Path, command:str, *, config, verbose=False, pure_mode=False ) -> list :
#     command_string = command # ToDo: clean up the args dict
#
#     # ToDo: merge config files -- locator, acl
#     ### figure out working directory, and add it to path
#
#     #subenv  = build_subenv( working_dir, config, pure_mode=pure_mode )
#
#     if verbose:
#         print( "SUBENV: " )
#         for item in sorted(subenv.items()):
#             print(str(item))
#
#     _, children = execute( command_string, env=subenv )
#     return children


#----------------------------------------------------------------------#
#
# def extension_handler( extension, filename ) :
#     return NotImplemented

# @export
# def run_open( filename, verbose=False, pure_mode=False ) -> list :
#
#     path_file = Path(filename).resolve().parents[0]
#
#     print("File:", filename)
#     extension=str(filename).split('.', maxsplit=1)[-1]
#     print("EXTENSION", extension)
#
#     # Select command by extension
#     command = ""
#     children = None
#
#     if extension == "yaml" :
#         run_service_yaml( path_file, verbose=verbose)
#         # Todo: keep service loop running
#     else:
#         command = extension_handler(extension, filename)
#
#         children = run_cmd( path_file, command, verbose=verbose, pure_mode=pure_mode )
#     return children
#

class Subprocess :
    '''coroutine for subprocesses'''
    __slots__ = (
        '_proc',
        'shell',
        'children'
    )

    def __init__( self, command: str, path: Path = None, env=None ) :
        self._proc = subprocess.Popen(
            command,
            env=env,
            cwd=str( path ),
            shell=True
        )
        self.shell = self._proc.pid

        ### collect child pids so they can be stored for later termination
        self.children = [process.pid for process in psutil.Process( self.shell ).children( recursive=True )]

    def orphan( self ) :
        '''kill the shell'''
        self._proc.terminate() #terminate exterior shell
        self._proc.wait()

    def close( self ) :
        '''kill the shell and the children'''
        self.orphan()
        kill_all( self.children )
        raise NotImplementedError

    def send( self ) :
        '''input to stdin'''
        raise NotImplementedError

    def __iter__( self ) :
        '''iterator protocol'''
        return self

    def __next__( self ) :
        '''block until output'''
        self._proc.wait()


#----------------------------------------------------------------------#

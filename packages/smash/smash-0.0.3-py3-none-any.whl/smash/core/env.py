#-- smash.core.env

"""
"""


from powertools import export
from powertools import AutoLogger
log = AutoLogger()
from powertools.print import *
from powertools import term

from pathlib import Path
from contextlib import contextmanager
from collections import OrderedDict
from collections import deque

import sys
import os
import subprocess
import psutil
import time


from .config import ConfigTree
from .config import SHELL_VARS_SECTION

from ..util.proc import Subprocess
from ..util.path import temporary_working_directory

#----------------------------------------------------------------------#

class MissingShellExportError( Exception ) :
    ''' not config nor its parents defined any exporter for shell variables '''


#----------------------------------------------------------------------#

################################
@export
class Environment:
    ''' represent the state of an environment where commands may be executed '''

    __slots__ = (
        'homepath',
        'pure',
        'parent',
        'simulation',

        'children',
        'results',
        'closed'
    )

    def __init__( self, homepath, *,
                  pure          = True,
                  parent        = None,
                  simulation    = True,
                  **kwargs ) :
        ''' homepath is the root of relative paths in the environment
            if
            if simulation is True, don't actually do anything; just print.
        '''

        self.homepath       = Path(homepath)
        self.pure           = pure
        self.parent         = parent
        self.simulation     = simulation

        self.children       = list()
        self.results        = deque()
        self.closed         = None


    ####################
    def build(self):
        ''' run all the exporters '''
        raise NotImplementedError()

    def validate( self ) :
        ''' check if the environment state satisfies constraints '''
        raise NotImplementedError()

    def initialize(self):
        ''' finalize preparation of the environment '''
        raise NotImplementedError()

    def teardown(self):
        ''' clean up the environment when it's no longer needed '''
        raise NotImplementedError()

    ####################
    @property
    def variables( self ) :
        ''' access to shell state variables '''
        raise NotImplementedError()

    ####################
    def run( self, *command ) -> Subprocess:
        ''' execute a command within the environment '''

        ### environment variables
        variables = self.variables

        ### execution path
        log.print( '\nWORKDIR: ', self.config.path )

        ### parse token expressions in command as if it were a key in the SHELL_VARS_SECTION section
        cmd_str = ' '.join( str( c ) for c in command )
        log.print('RAW CMD: ', cmd_str)
        cmd_str_parsed = self.config[SHELL_VARS_SECTION].evaluate( 'CMD', cmd_str, kro=self.config.parents ).replace( r'\\', r'\\' )
        log.print( 'COMMAND: ', cmd_str_parsed, '\n')

        ### execute
        with temporary_working_directory( self.config.path ):
            return Subprocess( cmd_str_parsed, self.config.path, variables )
                                                # todo: ^

    #################### context manager interfaces
    def __enter__( self ) :
        self.build( )
        self.validate( )
        self.initialize( )
        return self

    def __exit__( self, exc_type, exc_value, traceback ) :
        self.teardown( )


    #################### iterator/coroutine interfaces
    #todo: can an environment be represented as a coroutine? send commands in, yield results back out

    def __await__(self):
        return self
    def __iter__(self):
        return self
    def __next__(self):
        if self.closed:
            raise StopIteration(self.results)
        try:
            return self.results.popleft()
        except IndexError as e:
            return None

    def send(self, value):
        return self.run(value)

    def close(self):
        self.closed = True

    def throw(self, exc_type, exc_value=None, traceback=None):
        ''' raise exception inside of the __exit__ method? '''
        raise exc_type(self, exc_value, traceback)

    ####################

    def mkdir(self, path:Path) -> Path:
        ''' recursively create path if it doesn't exist.
            path must be relative, a branch of the homepath subtree.
            returns the absolute path that was created
        '''
        absolute_path = (self.homepath/path).resolve()

        absolute_path.mkdir(0o600)
        return absolute_path


    def rmfile( self, path: Path ):
        ''' recursively create path if it doesn't exist.
            path must be relative, a branch of the homepath subtree.
            returns the absolute path that was created
        '''
        absolute_path = (self.homepath / path).resolve()

        absolute_path.unlink()


#----------------------------------------------------------------------#



#----------------------------------------------------------------------#

@export
class ContextEnvironment( Environment ) :
    ''' Environment within which smash is running,
        could be an explicit smash instance,
        or some implicit unmanaged system environment
    '''
    __slots__ = ()

    def __init__( self, homepath=None, pure=False, **kwargs ) :
        if homepath is None:
            homepath = os.getcwd()
        super( ).__init__( homepath, **kwargs)



    @property
    def instance_template( self ) :
        ''' determine whether the context is an instance, and retrieve its template '''
        return None


    ####################
    def build( self ) :
        ''' do what? '''


    def validate( self ) :
        ''' defer to instance template '''


    def initialize( self ) :
        sys.path.append( str( self.homepath ) )
        os.chdir( str( self.homepath ) )

    def teardown( self ) :
        ''' do what? '''


    ####################
    @property
    def variables( self ) :
        return OrderedDict( os.environ )


    ####################
    def run( self, *command ) :
        raise NotImplementedError()

#----------------------------------------------------------------------#
@export
class InstanceEnvironment( Environment ) :
    ''' Environment within which smash is running,
        could be an explicit smash instance,
        or some implicit unmanaged system environment
    '''
    __slots__ = (
        'configtree',
    )

    def __init__( self, homepath=None, parent=None, pure=False, **kwargs ) :
        ''' either homepath or parent.homepath '''
        if homepath is None :
            homepath = parent.homepath

        super().__init__( homepath, pure=pure, **kwargs )
        try :
            self.configtree = ConfigTree.from_path( homepath )
            assert self.configtree.final
        except FileNotFoundError as e :
            self.configtree = ConfigTree( )
        except AssertionError as e :
            raise ConfigTree.NotFinalizedError( e )

        log.debug( 'CONFIGS:  ', self.configtree, '\n' )

    @property
    def instance_template( self ) :
        ''' determine whether the context is an instance, and retrieve its template '''
        return None

    ####################
    def build( self ) :
        ''' do what? '''

    def validate( self ) :
        ''' defer to instance template '''

    def initialize( self ) :
        sys.path.append( str( self.homepath ) )
        os.chdir( str( self.homepath ) )

    def teardown( self ) :
        ''' do what? '''

    ####################

    @property
    def config(self):
        return self.configtree.root

    @property
    def variables( self ) :
        from ..core.plugins import exporters

        try : # todo: refactor how environment export works. subenv should be the export sink key, and Exporters should push values into it. The virtual environment should just check that sink after exporters have been ran.
            export_subtrees = self.config.exports['Shell']['subenv']
        except KeyError :
            if self.config.is_pure :
                raise MissingShellExportError( str(
                    self.config.filepath ) + ' and its parents did not define any Exporters for pure virtual environment.' )
            else :
                print( "Warning: No Shell Exporter defined. Will use only exterior environment variables." )
                return OrderedDict()
        exporter = exporters['Shell']
        subenv = exporter( self.config, export_subtrees, 'subenv' ).export()

        result = OrderedDict()
        if not self.pure :
            result.update( os.environ )
        result.update( subenv )
        # log.info()
        # dictprint(result)
        return result

    def install_package( self ):
        pass


#----------------------------------------------------------------------#

SUBPROCESS_DELAY = 0.01

################################
@export
class VirtualEnvironment(Environment):
    ''' Environment that is launched as a child of the smash process
        shell variables are supplied by evaluating the 'Environment' __export__ process in the configtree
    '''
    __slots__ = (
        'configtree',
    )

    def __init__( self, instance:InstanceEnvironment, **kwargs ):
        self.configtree = instance.configtree
        homepath    = self.config.path
        super().__init__(homepath, pure=True, **kwargs)

    @property
    def config(self):
        return self.configtree.env

    ####################
    def build( self ) :
        ''' create config files '''
        from .plugins import exporters

        print(term.white('\nBUILD VIRTUAL ENVIRONMENT'))

        log.info( term.red( 'ENVIRONMENT KEY RESOLUTION ORDER' ) )

        listprint( self.config.key_resolution_order, pfunc=log.info )

        for name, target in self.config.exports.items():
            if name == 'Shell': continue
            exporter = exporters[name]

            for destination, sections in target.items():
                print(term.red('\nEXPORT'),' {:<10} {:<50} {:<10} {:<10}'.format(str(name), str(destination), str(sections), str(exporter)) )
                result = exporter(self.config, sections, destination).export()
        print(term.white('\n----------------'))


    def validate( self ) :
        pass

    def initialize( self ) :
        pass

    def teardown( self ) :
        pass


    ####################
    @property
    def variables( self ) :
        from ..core.plugins import exporters

        try : # todo: refactor how environment export works. subenv should be the export sink key, and Exporters should push values into it. The virtual environment should just check that sink after exporters have been ran.
            export_subtrees = self.config.exports['Shell']['subenv']
        except KeyError :
            if self.config.is_pure :
                raise MissingShellExportError( str(
                    self.config.filepath ) + ' and its parents did not define any Exporters for pure virtual environment.' )
            else :
                print( "Warning: No Shell Exporter defined. Will use only exterior environment variables." )
                return OrderedDict( )
        exporter    = exporters['Shell']
        subenv      = exporter( self.config, export_subtrees, 'subenv' ).export()

        result = OrderedDict()

        if not self.pure :
            result.update( os.environ )

        result.update( subenv )
        # log.info()
        # dictprint(result)
        return result


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

# todo: fix 'No cio_test package found.'
# https://github.com/conda/conda/issues/5356



################################
@export
class CondaEnvironment( VirtualEnvironment ) :
    ''' construct a conda environment, and run commands inside it '''
    __slots__ = ()

    def _manage(self, command, *arguments, **kwargs):
        import conda
        from conda.cli import python_api

        log.print('manage ', self.config)
        python_api.run_command( command, *arguments, **kwargs )

        raise NotImplementedError()

    ####################
    def build( self ) :
        ''' construct a conda environment '''

    def validate( self ) :
        ''' defer to instance template '''

    def initialize( self ) :
        ''' '''

    def teardown( self ) :
        ''' '''

    ####################
    @property
    def variables( self ) :
        raise NotImplementedError

    ####################
    def run( self, *command ) :
        raise NotImplementedError


#----------------------------------------------------------------------#

################################
@export
class DockerEnvironment( Environment ) :
    '''construct an environment inside a docker container, and run commands inside it'''
    __slots__ = ()

    def __init__( self, homepath, **kwargs ) :
        super( ).__init__( homepath, **kwargs )

        raise NotImplementedError()


    ####################
    def build( self ) :
        ''' construct the docker image '''


    def validate( self ) :
        ''' defer to instance template '''


    def initialize( self ) :
        ''' boot the docker image'''


    def teardown( self ) :
        ''' destroy the docker image'''


    ####################
    @property
    def variables( self ) :
        raise NotImplementedError()

    ####################
    def run( self, *command ) :
        raise NotImplementedError()


#----------------------------------------------------------------------#
@export
class RemoteEnvironment( Environment ):
    ''' connect to a remote environment using ssh'''
    __slots__ = ()

    def __init__( self, url, remote:Environment, **kwargs ) :
        super( ).__init__( remote.homepath, **kwargs )
        self.url = url

        raise NotImplementedError()

    ####################
    def build( self ) :
        ''' '''

    def validate( self ) :
        ''' '''

    def initialize( self ) :
        ''' '''

    def teardown( self ) :
        ''' '''

    ####################
    @property
    def variables( self ) :
        raise NotImplementedError()

    ####################
    def run( self, *command ) :
        raise NotImplementedError()


#----------------------------------------------------------------------#

builtin_environment_types = {
    'context'   : ContextEnvironment,
    'subenv'    : VirtualEnvironment,
    'conda'     : CondaEnvironment,
    'docker'    : DockerEnvironment,
    'remote'    : RemoteEnvironment
}

#----------------------------------------------------------------------#

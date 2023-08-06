#-- smash.core.handler

"""

"""


from powertools import AutoLogger
log = AutoLogger()

################################

from pathlib import Path
from .config import Config
from .env import Environment

from powertools import term
from powertools.print import rprint, listprint, dictprint
from pprint import pprint, pformat

from ..util.meta import classproperty

from pathlib import Path
from collections import OrderedDict
from contextlib import suppress

from powertools import export

#----------------------------------------------------------------------#

@export
class NoHandlerMatchedError(Exception):
    '''no handler picked up the file as a target it could provide the command string for'''

@export
class MissingTargetFileError( Exception ) :
    ''' tried to run a file that doesn't exist '''


@export
class Handler:
    ''' base class for setting up an action to be executed using a target file '''

    def __init__( self,
                  target:Path,
                  arguments:list,
                  env:Environment
                  ) -> None:
        self.target     = target
        self.arguments  = arguments
        self.env        = env

    def __run__( self, target: Path, arguments, env: Environment, *, ctx=None ):
        ''' this method is nominally static '''
        raise NotImplementedError()

    def run( self, ctx ) :
        ''' implement the __run__ magic method on subclasses '''
        #todo: this should return a future
        return self.__run__( self.target, self.arguments, self.env, ctx=ctx )


#----------------------------------------------------------------------#

@export
class SubprocessHandler( Handler ) :
    ''' execute the target as-is'''

    def __run__( self, command, arguments, env: Environment, *, ctx=None ) :
        proc = env.run(command, *arguments)
        return next(proc) # wait for termination


#----------------------------------------------------------------------#

@export
class YamlispHandler( Handler ) :
    ''' this allows using the python interpreter defined by the virtual environment'''

    def __run__( self, target: Path, arguments, env: Environment, *, ctx=None ) :
        ''' read the file and do something with it'''

        if not Path( target ).exists() :
            raise MissingTargetFileError( target )

        # if target != env.config.filepath:
        env.config.tree.new_env( target )
        log.print('')

        subcommand, subarguments = '__main__', []
        with suppress( IndexError ) :
            subcommand = arguments[0]
        with suppress( IndexError ) :
            subarguments = arguments[1: ]

        from .yamlisp import run_yamlisp
        return run_yamlisp(env, env.config, subcommand, subarguments, g_kwargs=OrderedDict())
        # todo: support kwargs in handlers





#----------------------------------------------------------------------#

@export
class Daemonizer( SubprocessHandler ):
    RESTART_DELAY = 5
    def __run__( self, command, arguments:list, env: Environment, *, ctx=None ) :
        import time
        while True:
            subcommand = Path( arguments[0] )
            subarguments = arguments[1:]
            log.info(term.dpink('subcommand:'), f' {subcommand} {str(*subarguments)}')
            proc = super().__run__( subcommand, subarguments, env, ctx=ctx )
            time.sleep(self.RESTART_DELAY)


#----------------------------------------------------------------------#

@export
class ToolHandler( Handler ) :
    '''command is a tool invocation'''

    def __run__( self, command, arguments, env: Environment, *, ctx=None ) :
        env.run( command, *arguments )

@export
class MouthHandler( Handler ) :
    '''print fortune'''

    def __run__( self, command, arguments, env: Environment, *, ctx=None ) :
        env.run( command, *arguments )


#----------------------------------------------------------------------#

@export
class ScriptHandler( Handler ) :
    '''execute the script using its appropriate interpreter'''
    __interpreter__ = NotImplemented

    def __run__( self, target: Path, arguments, env: Environment, *, ctx=None ) :
        env.run( self.__interpreter__ + ' ' + str( target ), arguments )

@export
class BashHandler( ScriptHandler ) :
    '''this depends on a path to bash being defined in one of the config files. it could be the host, or a bash package'''
    __interpreter__ = 'bash'

@export
class BatchHandler( ScriptHandler ) :
    __interpreter__ = 'cmd'

@export
class PythonHandler( ScriptHandler ) :
    '''this allows using the python interpreter defined by the virtual environment'''
    __interpreter__ = 'python'

#----------------------------------------------------------------------#

@export
class ConvertXML( Handler ) :
    ''' produce yaml file containing equivalent to input xml'''

    def __run__( self, target: Path, arguments, env: Environment, *, ctx=None ) :
        log.info('paths to convert: ', arguments)

        from ..util import yaml, xml
        for path in map(Path, arguments):

            data = xml.load(path)
            log.info(f'with {path}: ', len( list( data['locator']['DATABASES']['db'] ) ) )
            # listprint(data['locator']['DATABASES']['db'].items())
            purified_data = xml.convert_xmldict(data)
            output_path = path.parents[0] / f'{path.name}.yml'
            yaml.dump(output_path, purified_data)


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

### last in first out; use the last handler whose key regex matches the filename
builtin_handlers            = OrderedDict()
builtin_handlers['.*']          = SubprocessHandler # default

#todo: can these subcommands be integrated with click?
builtin_handlers['begin']       = Daemonizer
builtin_handlers['with']        = ToolHandler
builtin_handlers['mouth']       = MouthHandler
builtin_handlers['xml']         = ConvertXML

builtin_handlers['.*\.yml']    = YamlispHandler
builtin_handlers['.*\.yaml']   = YamlispHandler

builtin_handlers['.*\.sh']     = BashHandler
builtin_handlers['.*\.bat']    = BatchHandler
builtin_handlers['.*\.py']     = PythonHandler


#----------------------------------------------------------------------#

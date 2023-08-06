#-- smash.core.instance

"""

"""

from powertools import AutoLogger
log = AutoLogger()

################################


from powertools import term
from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from pathlib import Path
from shutil import copyfile
from inspect import getmro
from contextlib import suppress
from itertools import chain

from ..util.meta import classproperty
from powertools import export
from .config import Config
from .env import InstanceEnvironment
from ..util.path import temporary_working_directory
from ..util.proc import Subprocess

from .. import templates

import wget
from . import platform
Platform = platform.match()

from .pkg import Miniconda

#----------------------------------------------------------------------#

# this is where I can begin to flesh out the idea of config files being actual classes.

# todo: use cookiecutter to deploy an instance


@export
class InstanceTemplate :
    ''' template specifying an instance structure '''

    __slots__ = ('instance',)

    def __init__( self, instance ) :
        self.instance=instance

#----------------------------------------------------------------------#

@export
class SmashTemplate( InstanceTemplate ) :
    ''' procedure for creating a new instance directory '''

    __slots__ = ()
    def __init__( self, homepath: Path, **kwargs ) :


        log.print( term.pink( '\ncreating new instance in current directory... '), homepath.name )

        ###
        Path( homepath ).mkdir( 0o600 )
        self.write_root( homepath )

        ### inherit context as a parent from kwargs
        instance = InstanceEnvironment( homepath, **kwargs )
        super().__init__(instance)
        config = self.instance.configtree.env

        ###
        log.print( term.pink( '\ncreating subdirectories... ' ) )
        self.create_pathsystem( config )

        ###
        log.print( term.pink( '\ninstalling smash prerequisites... ' ) )
        self.install_default_packages( config )

        ###
        log.print( term.pink( '\ninstalling self-contained python...' ) )
        with Miniconda(self.instance, config) as mc:
            mc.download()
            mc.install()

        print(mc)

        ###
        # log.print( term.pink( '\nattempting to register new instance with network index' ) )
        # self.register_instance()


    ################################
    @staticmethod
    def write_root( homepath: Path, root_file=None ) :
        ''' strap your boots with hard-coded paths '''

        if root_file is None :
            src = str( templates.INSTANCE_CONFIG )
            dst = str( Path( homepath ) / templates.ROOT_YAMLISP )
            print( term.cyan('writing root config: '), term.dyellow(src), "-->", term.dyellow(dst), '\n' )
            copyfile( src, dst )

            src = str( templates.SMASH_PY )
            dst = str( Path( homepath ) / templates.SMASH_PY.name  )
            print( term.cyan( 'writing smash.py: ' ), term.dyellow( src ), "-->", term.dyellow( dst ), '\n' )
            copyfile( src, dst )


    ################################
    def create_pathsystem( self, config:Config ) :
        ''' create directories in config's path and pkg sections '''

        paths = chain(
            config['path'].allpaths(),
            config['pkg'].allpaths(),
        )
        for key, path in paths:
            with suppress( FileExistsError ) :
                log.info( term.pink( 'MKDIR: ' ), f"{str(path):<16}" )
                absolute_path = self.instance.mkdir( path )


    ################################
    def install_default_packages( self, config:Config ):
        ''' copy additional yamlisp files '''
        self.install_package( config, templates.PYTHON, 'PYTHON' )

        host_config = platform.switch(self.win_host_config, self.nix_host_config, self.mac_host_config)
        self.install_package( config, host_config, 'HOST' )

        self.install_package( config, templates.NET, 'NET' )


    def install_package(self, config:Config, template_path, pkg_name):
        src = str( template_path / templates.PKG_YAMLISP )
        dst = str( Path(config['pkg'][pkg_name]) / templates.PKG_YAMLISP )

        log.print( term.cyan('writing ',pkg_name,' package config: '),
                   '',term.dyellow(src),
                   ' --> ', term.dyellow(dst),
                   '\n')
        copyfile( src, dst )

        self.instance.configtree.add_node(Path(dst))




    def register_instance(self):
        ''' attempt to contact a configured network index and register the instance name '''


#----------------------------------------------------------------------#



#----------------------------------------------------------------------#

builtin_templates = {
    'smash' : SmashTemplate,
}

#----------------------------------------------------------------------#

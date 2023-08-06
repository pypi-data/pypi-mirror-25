#-- smash.core.pkg

"""
package types,
"""

from powertools import AutoLogger
log = AutoLogger()
from powertools import term
from powertools import assertion
from powertools import export

from pathlib import Path

from shutil import rmtree

import conda

from .tool import Installer


#----------------------------------------------------------------------#

@export
class PackageType:
    '''abstract monad for defining packaging semantics'''

    __slots__ = ('instance',)
    def __init__(self, instance):
        self.instance = instance


################################

@export
class Application( PackageType ):
    ''' non-reusable, end-user code
    '''


class Library( PackageType ):
    ''' nice, reusable code
    '''


################################

@export
class Account( PackageType ):
    ''' information for a unique client
        user definitions and permissions
    '''


@export
class Host( PackageType ):
    ''' configuration for a uniquely-identifyable node on the network
        define which abstract resources are available,
        and the absolute position of those resources
    '''


################################

@export
class Resource( PackageType ):
    ''' abstract local system resource, which can be instantiated by the host
    '''

@export
class Network( Resource ):
    ''' abstract remote network resource
    '''

@export
class NetworkIndex( Network ) :
    ''' remote service that can be used to register and discover other remote resources
    '''


################################

@export
class PackageIndex( Network ) :
    ''' configuration for obtaining smash packages
        package index could be on the local filesystem or the network, depending on host
    '''

@export
class PipPackageIndex( PackageIndex) :
    ''' configuration for obtaining pip-compatible packages
    '''

@export
class CondaPackageIndex( PackageIndex ) :
    ''' configuration for obtaining conda packages
    '''

@export
class FTPPackageIndex( PackageIndex ) :
    ''' Source of packages on a remote ftp server
    '''


################################

@export
class Data( Resource ) :
    ''' abstract database definitions
        associated loader tasks
    '''

@export
class DataStore( Data ) :
    ''' a specific instance of database state
    '''


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

@export
class Package(Installer) :
    ''' base class for managing version-controlled modules on a smash instance
        provides an additional hook for importing plugins
    '''
    __pkg__ = [Library]



################################

@export
class Python( Package ):
    ''' install standard python
    '''


@export
class Miniconda( Python ):
    ''' install miniconda
    '''

    source_url          = 'https://repo.continuum.io/miniconda/'
    filename_windows    = 'Miniconda3-latest-Windows-x86_64.exe'
    filename_linux      = 'Miniconda3-latest-Linux-x86_64.sh'

    @property
    def download_destination( self ) -> Path:
        return Path(self.config['pkg']['PYTHON']).resolve()


    @property
    def install_destination( self ) -> Path :
        python_pkg_path = Path( self.config['pkg']['PYTHON'] ).resolve()
        python_name     = self.config.tree[python_pkg_path]['python']['NAME']

        return python_pkg_path / python_name


    def command_windows( self ) :
        return [
            (self.download_destination / self.filename_windows).resolve(),
            '/S', # silent mode
            '/InstallationType=JustMe',
            '/AddToPath=0',
            '/RegisterPython=0',
            f'/D={str(self.install_destination)}'
        ]

    def command_linux( self ) :
        raise NotImplementedError

    def command_mac( self ) :
        raise NotImplementedError


    def __exit__( self, exc_type=None, exc_value=None, exc_tb=None ) :
        '''clean up installation artifacts'''

        ### delete installer
        (self.download_destination / self.installer_filename).unlink()

@export
class Anaconda( Miniconda ):
    ''' install anaconda
    '''


################################

@export
class Shell( Package ) :
    ''' interface for controlling a shell program
        use this to provide a wrapper for shell commands to enable tracking and versioning of state
    '''


@export
class BatchCMD( Shell ) :
    ''' implement wrappers for windows batch script
    '''


@export
class Bash( Shell ) :
    ''' implement wrappers for bash shell
    '''


@export
class Xonsh( Shell ) :
    ''' implement wrappers for xonsh shell
    '''


################################

@export
class Git( Package ):
    pass


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#


################################
builtin_package_types = {
    'app'       : Application,
    'lib'       : Library,

    'acct'      : Account,
    'host'      : Host,

    'res'       : Resource,
    'net'       : Network,

    'idx-net'   : NetworkIndex,
    'idx-pkg'   : PackageIndex,
    'idx-pip'   : PipPackageIndex,
    'idx-conda' : CondaPackageIndex,
    'idx-ftp'   : FTPPackageIndex,

    'data'      : Data,
    'store'     : DataStore
}


################################
builtin_packages = {
    'Python'    : Python,
    'Miniconda' : Miniconda,
    'Anaconda'  : Anaconda,
    'Git'       : Git,
    'Shell'     : Shell,
    'BatchCMD'  : BatchCMD,
    'Bash'      : Bash,
    'Xonsh'     : Xonsh,
}


#----------------------------------------------------------------------#



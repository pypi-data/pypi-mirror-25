#-- smash.core.exporter

"""
write output files from compiled configtree node
"""

from powertools import export
from powertools import AutoLogger
log = AutoLogger()

################################

import sys

from collections import OrderedDict
from collections import namedtuple
from collections import defaultdict
from ordered_set import OrderedSet
from pathlib import Path


from .config import Config
from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from ..util.meta import classproperty


#-------------------------------------------------------------------------------------------------#

#todo: refactor so that subclasses are providing init methods
@export
class Exporter:
    ''' methods for writing contents of configtree to an output file'''

    @classproperty
    def __key__(cls):
        return cls.__name__

    def __init__( self, config:Config, sections, destination ) :
        self.config         = config
        self.sections       = sections
        self.destination    = destination


    def write( self, config:Config, sections:list, destination:str ):
        raise NotImplementedError


    def export( self, ) :
        return self.write(self.config, self.sections, self.destination)


################################


#-------------------------------------------------------------------------------------------------#

@export
class ExportShell( Exporter ):

    class AmbiguousKeyError( Exception ) :
        ''' two sections exported to the same destination have matching keys'''


    pathlist_delimiter = ';' if sys.platform=='win32' else ':'

    @classmethod
    def pathlist2string(cls, paths:list) -> str:
        pathlist = list()
        for value in paths:
            if isinstance(value, str):
                pathlist.append(value)
                continue
            if isinstance(value, list):
                pathlist.extend(value)
                continue
            raise TypeError("Can't append to pathlist: "+str(value)+" | "+str(type(value)))

        return cls.pathlist_delimiter.join(OrderedSet(pathlist))


    def write( self, config: Config, sections:list, destination:None ) -> OrderedDict:
        subenv      = OrderedDict()
        keysources  = OrderedDict()

        for section in sections:
            for key, value in config[section].allitems():
                if key not in subenv:
                    if isinstance(value, str):
                        subenv[key]     = str(value)
                        keysources[key] = section
                    elif isinstance(value, list):
                        subenv[key]     = self.pathlist2string( value )
                        keysources[key] = section
                    else:
                        raise TypeError('Invalid environment value',
                                    namedtuple('_',['section', 'key', 'value', 'type' ])
                                                    (section, key, str(value), str(type(value))))
                    log.info( out.pink( 'ExportShell' ), " {:<20} = {:64}".format(str(key), subenv[key])  )
                else:
                    raise self.AmbiguousKeyError(
                        namedtuple( '_', ['conflicting_sections', 'key', 'values', 'config', 'destination'] )(
                            (section, keysources[key]),
                            key,
                            (value, subenv[key]),
                            str( config ),
                            destination
                        )
                    )
        return subenv


#-------------------------------------------------------------------------------------------------#

################################
@export
class ExportShellScript( Exporter ) :
    def write( self, config: Config, sections, destination ) -> None :
        raise NotImplementedError

################################
@export
class ExportShellScriptCMD( ExportShellScript) :
    def write( self, config: Config, sections, destination ) -> None :
        raise NotImplementedError

################################
@export
class ExportShellScriptBASH( ExportShellScript ) :
    def write( self, config: Config, sections, destination ) -> None :
        raise NotImplementedError


#-------------------------------------------------------------------------------------------------#
@export
class ExportDebug( Exporter ) :
    def write( self, config: Config, sections, destination ) -> None:
        raise NotImplementedError


#-------------------------------------------------------------------------------------------------#
@export
class ExportYAML( Exporter ) :
    def write( self, config: Config, sections, destination ) -> None:
        raise NotImplementedError


#-------------------------------------------------------------------------------------------------#
@export
class ExportXML( Exporter ) :
    def write( self, config: Config, sections, destination ) -> None:
        raise NotImplementedError


#-------------------------------------------------------------------------------------------------#
@export
class ExportINI( ExportShell ) :

    pathlist_delimiter = ','

    def write( self, config: Config, sections: list, destination: str ) :
        from configparser import ConfigParser

        inidata      = ConfigParser( )
        for section in sections :
            inidata.setdefault(section,OrderedDict())
            log.info( out.red( 'ExportINI Section [' ), "{}".format( str( section )), out.red(']') )
            for key, value in config[section].allitems( ) :
                if isinstance( value, str ) :
                    inidata[section][key] = "'"+str( value )+ "'"
                elif isinstance( value, list ) :
                    inidata[section][key] = "'"+self.pathlist2string( value )+"'"
                else :
                    raise TypeError( 'Invalid environment value',
                                     namedtuple( '_', ['section', 'key', 'value', 'type'] )
                                     ( section, key, str( value ), str( type( value ) ) ) )
                log.info( "    {:<20} = {:64}".format( str( key ), inidata[section][key] ) )

        outpath = Path(destination)
        # print('outpath', outpath, outpath.parent)
        for path in reversed(outpath.parents):
            if not path.exists():
                # print("MKDIR", path)
                path.mkdir()
        with open( destination, 'w' ) as outfile :
            # print("write to destination", destination, outfile)
            inidata.write( outfile)


#-------------------------------------------------------------------------------------------------#

# todo: change sys.platform checks to environment platform checks

builtin_exporters = {
    'Shell'         : ExportShell,
    'ShellScript'   : ExportShellScriptCMD if sys.platform=='win32'
                 else ExportShellScriptBASH,
    'Debug'         : ExportDebug,
    'YAML'          : ExportYAML,
    'XML'           : ExportXML,
    'INI'           : ExportINI
}

#-------------------------------------------------------------------------------------------------#

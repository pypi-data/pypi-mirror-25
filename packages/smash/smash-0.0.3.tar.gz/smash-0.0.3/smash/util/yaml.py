#-- smash.sys.yaml

'''
process yaml files
'''

from powertools import AutoLogger
log = AutoLogger()
from collections import OrderedDict
from pathlib import Path

import ruamel.yaml as yaml

try :
    from ruamel.yaml import CLoader as Loader, CDumper as Dumper
except ImportError :
    from ruamel.yaml import Loader, Dumper
import sys

yaml.representer.RoundTripRepresenter.add_representer(
    OrderedDict,
    yaml.representer.RoundTripRepresenter.represent_ordereddict )

from ruamel.yaml.comments import CommentedMap

# YAML Anchors, references, nested values    - https://gist.github.com/bowsersenior/979804

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    try :
        __all__.append( obj.__name__ )
    except AttributeError :
        __all__.append( obj.__main__.__name__ )
    return obj

#----------------------------------------------------------------------#

# OrderedDictYYAMLLoader - https://gist.github.com/enaeseth/844388
class OrderedDictYAMLLoader(  Loader ) :
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__( self, *args, **kwargs ) :
        Loader.__init__( self, *args, **kwargs )

        self.add_constructor( u'tag:yaml.org,2002:map', type( self ).construct_yaml_map )
        self.add_constructor( u'tag:yaml.org,2002:omap', type( self ).construct_yaml_map )

    def construct_yaml_map( self, node ) :
        data = OrderedDict( )
        yield data
        value = self.construct_mapping( node )
        data.update( value )

    def construct_mapping( self, node, deep=False ) :
        if isinstance( node, yaml.MappingNode ) :
            self.flatten_mapping( node )
        else :
            raise yaml.constructor.ConstructorError(
                None, None,
                'expected a mapping node, but found %s' % node.id,
                node.start_mark )

        mapping = OrderedDict( )
        for key_node, value_node in node.value :
            key = self.construct_object( key_node, deep=deep )
            try :
                hash( key )
            except TypeError as exc :
                raise yaml.constructor.ConstructorError( 'while constructing a mapping',
                                                         node.start_mark, 'found unacceptable key (%s)' % exc,
                                                         key_node.start_mark )
            value = self.construct_object( value_node, deep=deep )
            mapping[key] = value
        return mapping


#----------------------------------------------------------------------#

def load( filename:Path ) :
    result = None
    with filename.open( ) as file:
        result = yaml.load(file, Loader=OrderedDictYAMLLoader )

    return result



#----------------------------------------------------------------------#


def make_yml() :
    yml = yaml.YAML()
    yml.explicit_start      = False
    yml.indent              = 2
    yml.block_seq_indent    = 0
    yml.typ                 = 'safe'
    yml.tags                = False


    return yml


#----------------------------------------------------------------------#


#----------------------------------------------------------------------#

def dump( filename: Path, data ) :
    yml = make_yml()
    with open( str(filename), 'w' ) as file :
        yaml.dump( data, file, Dumper=yaml.RoundTripDumper, indent=2, block_seq_indent=0, explicit_start=False, tags=None, canonical=False)
    yml.dump( data, sys.stdout  )

#----------------------------------------------------------------------#

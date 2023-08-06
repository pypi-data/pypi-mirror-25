
#-- smash.sys.yaml

'''
process yaml files
'''

from powertools import AutoLogger
log = AutoLogger()
from powertools import term
from powertools import GreedyOrderedSet

from collections import OrderedDict
from pathlib import Path
import types

from ..core.config import getdeepitem
from ..core.config import ConfigSectionView

import xmltodict
from ruamel.yaml.comments import CommentedMap


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

class UnknownRFormatSectionType( Exception ) :
    ''' convert config section into xmldict'''


################################
def rformat_xml( config, *sections, depth=0, inheritance_depth=2 ) :
    result = None
    indent = depth * ('  ' if depth%2==1 else ': ')

    # log.info('FORMAT: ', config, ' | ', sections)
    section = getdeepitem( config, tuple(sections) )

    if isinstance( section, str ) :
        if isinstance( section, str ) :
            log.info( indent,
                      term.dpink( 'Scalar: ' ),
                      term.dpink( ' | ' ),
                      str( section )
                      )
        result = section

    elif isinstance( section, ConfigSectionView ) :
        log.info( indent, term.pink( 'Mapping ' ), section.config, ' | ', section.section_keys )

        result = OrderedDict()
        try :
            # log.info( indent, term.cyan( '1 '),)
            if depth <= inheritance_depth:
                section_items = list( section.allitems() )
            else:
                section_items = list(section.items())
            # for node in config.parents:
            #     items = list()

        except RecursionError as e :
            raise RecursionError( e, str( section ) ) #from None

        for key, value in section_items :
            log.info( indent,
                      term.dpink( 'Item: ' ),
                      term.cyan(key),
                      term.dpink( ' | ' ),
                      term.dcyan(str( v for v in value ) if isinstance( value, (list, tuple) ) else str( value ))
                      )

            if isinstance( value, str ) :
                result[key] = value
            else :
                result[key] = rformat_xml( config, *sections, key, depth=depth + 1, inheritance_depth=inheritance_depth )

    elif isinstance( section, (list, tuple, types.GeneratorType) ) :
        result = list()
        log.info( indent, term.pink( 'Sequence ' ), len(list( str( s ) for s in section ) ))
        for i, value in enumerate( section ) :

            ###
            log.info( indent,
                       term.dpink( 'Value: ' ),
                       term.dyellow(str( v for v in value ) if isinstance( value, (list, tuple) ) else str( value ))
                       )


            if isinstance( value, str ) :
                result.append( value )
            else :

                result.append( rformat_xml( config, *sections, i, depth=depth + 1, inheritance_depth=inheritance_depth ) )
    else :
        raise UnknownRFormatSectionType( section )

    return result


################################
def convert_xmldict( data, depth=0 ) :
    ''' convert file containing XML to lists/dicts '''

    result = None
    indent = depth * 4 * ' '

    if isinstance(data, str):
        log.info( indent,
                  term.cyan( 'Scalar: ' ),
                  term.cyan( ' | ' ),
                  str( data )
                  )
        result = data

    if isinstance( data, dict ) :
        log.info( indent, term.cyan( 'Mapping ' ), type(data))
        result = CommentedMap()
        for key, value in data.items() :
            log.info( indent,
                       term.cyan( 'Mapping Item: ' ),
                       key,
                       term.cyan( ' | ' ),
                       str( v for v in value ) if isinstance( value, (list, tuple) ) else str( value )
                       )

            if isinstance( value, str ) :
                result[key] = value
            else :
                result[key] = convert_xmldict( data[key],depth=depth + 1 )



    if isinstance( data, (list, tuple) ) :
        log.info( indent, term.cyan('Sequence '), type( data ) )
        result = list()
        for i, value in enumerate(data):
            log.info( indent,
                       term.cyan( 'Sequence Item: ' ),
                       str( v for v in value ) if isinstance( value, (list, tuple) ) else str( value )
                       )

            if isinstance( value, str ) :
                result.append( value )
            else :
                result.append( convert_xmldict( data[i], depth=depth + 1 ) )

    return result

#----------------------------------------------------------------------#

dump_args = OrderedDict(
    pretty=True,
    full_document=False,
    attr_prefix='~',
    short_empty_elements=True
)

def load( filename: Path ) :
    with filename.open() as xmlfile :
        data = xmltodict.parse( xmlfile.read(), attr_prefix='~' )
    return data


def dump(filepath: Path, data, kwargs=dump_args ):
    with open(str(filepath), 'w') as file:
        xmltodict.unparse(data, output=file, **kwargs )
        xmltodict.unparse(data, **kwargs)

#----------------------------------------------------------------------#

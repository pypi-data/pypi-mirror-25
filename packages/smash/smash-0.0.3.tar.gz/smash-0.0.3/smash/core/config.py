#-- smash.core.config

"""
manipulate configuration files
yamlisp attempt #2
"""

#todo: separate out the yaml processing from the core config concepts; configtree should be a metaclass representing configs as classes

from powertools import AutoLogger
log     = AutoLogger()


################################

import os
import re

from collections import defaultdict
from collections import ChainMap
from collections import OrderedDict
from collections import namedtuple
from collections import deque
from ordered_set import OrderedSet

from functools import reduce
from itertools import chain
from itertools import starmap
from contextlib import suppress
from copy import deepcopy
from pathlib import Path
import types

from ..util.yaml import load as load_yaml
from ..util.path import stack_of_files
from ..util.path import temporary_working_directory
from ..util.path import try_resolve
from ..util.path import find_yamls
from . import platform

from powertools import term
from powertools.print import listprint, dictprint, rprint, pprint, pformat, add_pprint
from powertools import GreedyOrderedSet
from powertools import qualname

from smash.core.constants import CONFIG_PROTOCOL

from powertools import export

PATH_VARS_SECTION   = 'path'
SHELL_VARS_SECTION  = 'var'

#----------------------------------------------------------------------#




def listdefault( l, key, default ) :
    try :
        return l[int( key )]
    except IndexError as e:
        raise IndexError(e, l, key) from None
        # l.append( default )
        # return l[-1]

def getdeepitem( data, keys, kro=() ) :
    ''' convert nested index access to a list of keys
        supports passing along the key resolution order for configsectionview lookups
    '''

    def getlayer( d, key ) :
        if isinstance( d, ConfigSectionView ) :
            return d.setdefault( key, OrderedDict(), kro=kro )
        #elif isinstance( d, dict ):
        elif isinstance( d, (dict, Config) ) :
            return d.setdefault( key, OrderedDict() )
        elif isinstance( d, (list, tuple)):
            return listdefault( d, key, [] )
        elif d is None:
            return OrderedDict()     # magical container dummyplug
        raise TypeError(d, key)


    return reduce( getlayer, #d[key],
                   keys, data )






#----------------------------------------------------------------------#

# todo: a config could be in a python module instead of a yaml file

@export
class Config:
    ''' A single configuration structure expressed as arbitarily nested dictionaries and lists
        config[section][key]
        sections may be nested within sections arbitrarily deep
        config[section1][section2][key]
        the interpretation of the keys is delegated to the ConfigSectionView
    '''

    class ProtocolError(Exception):
        ''' Yaml file did not have the correct protocol '''

    class EmptyFileWarning(Exception):
        ''' May wish to ignore blank config files '''

    class SubstitutionKeyNotFoundError(Exception):
        ''' expression token contained a key whose value could not be found during regex substitution '''

    class SubstitutionValueTypeError(Exception):
        ''' couldn't value the type of the value obtained from token substitution'''

    class TokenExpressionError(Exception):
        ''' $ tokens are scalar substitutions, @ tokens are sequence extensions '''

    class TokenRecursionError(Exception):
        ''' RecursionError occured while performing token substitution '''

    class InheritSelfError(Exception):
        ''' config is its own parent '''

    class InheritLoopError(Exception):
        ''' config has a parent whose parent is config '''

    class ParentNotFound(Exception):
        ''' filepath in __inherit__ list could not be found '''

    class MissingCommandWordError(Exception):
        ''' yamlisp s-expressions must contain at least a command word'''

    class YamlispKwargDuplicate(Exception):
        ''' duplicate keys from dictionaries on the same line of a yamlisp script'''

    class DuplicateScriptLineName(Exception):
        ''' two s-expressions in a yamlisp command word have the same key '''

    class DelayedEvaluationTokenNotDuringScript( Exception ) :
        ''' avoid infinite substitution loop for delayed tokens'''


    ####################
    def __init__( self, tree=None ) :

        self.filename   = None
        self.path       = None
        self.filepath   = None

        self._yaml_data     = None
        self._final_cache   = OrderedDict( )

        self.tree       = tree


    ####################
    @classmethod
    def from_yaml( cls, target_file: Path, tree=None ) :
        self = cls( tree=tree )
        self.load( target_file )
        return self


    ####################
    def load( self, target: Path ) :

        self.filepath   = target.resolve()
        self.path       = target.parents[0]
        self.filename   = target.name

        self._yaml_data  = load_yaml( target )
        # todo: validate magic keys and immediately raise exception if not a compatible format

        if self._yaml_data is None:
            raise Config.EmptyFileWarning(self.filepath)

        for section_name in self._yaml_data.keys( ) :
            self._final_cache[section_name] = OrderedDict( )

        try:
            assert self.protocol == CONFIG_PROTOCOL
        except KeyError as e:
            raise Config.ProtocolError('Missing __protocol__', str(self))
        except AssertionError as e:
            raise Config.ProtocolError('Protocol version mismatch')

        log.dinfo( 'Config.load = ', term.yellow(self.filepath) )

        #print( 'parents:', self.__inherit__ )

        # todo: straighten out this manual addition of self to the configtree
        if self.tree is not None :
            self.tree.nodes[self.filepath] = self

        self.load_parents()
        log.debug(term.yellow('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~done: '), self.filepath,'\n')

    def load_parents(self):
        log.debug( 'load_parents ',term.dyellow(self.filepath), ' ', self.__inherit__)
        for path in starmap( lambda k,p: Path(p).resolve(), self.__inherit__.items() ):

            log.debug( term.pink('inherit_path: '), path)
            if not path.exists():
                raise Config.ParentNotFound(
                    '\n'+term.dcyan('Config:')+ f' {str(self.filepath)}'
                   +'\n'+term.dcyan('Parent:')+ f' {str(path)}'
                   +''   # raise Config.ParentNotfound
                )
            if path not in self.tree.nodes:
                self.tree.add_node(path)
                self.tree[path].load_parents()


    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    def __str__( self ) :
        return "".join( str( s )
            for s in [
                '<', self.__class__.__name__, ': ', self.filepath, '>'
            ] )

    __pprint__= __str__
    __repr__ = str

    @property
    def name( self ) :
        return self._yaml_data['__name__']


    @property
    def protocol( self ) :
        return self._yaml_data['__protocol__']

    @property
    def version( self ) :
        return self._yaml_data['__version__']

    @property
    def is_pure( self ) :
        with suppress(KeyError):
            return bool(self._yaml_data['__pure__'])
        return True


    ####################
    @property
    def __inherit__( self ) -> OrderedDict :
        ''' compute this node's immediate parents from the config's __inherit__ list
            a value in the list may either be a string or a dictionary
            if it is a string, it refers to the path of a prante config file
            if dictionary, the keys must be Platform names,
                and the values are parent config file paths
        '''
        # todo: ConfigSectionView needs refactoring

        ### try to get the raw __inherit__ list
        try :
            parent_items = self._yaml_data['__inherit__']
        except KeyError as e :
            parent_items = list()
        except TypeError as e:
            parent_items = list()

        # log.info( term.blue( 'parent items: ' ), parent_items )
        ### if a dictionary is provided, the keys may be used as aliases for the path inside token expressions
        if isinstance(parent_items, dict):
            parent_aliases  = deepcopy(list(parent_items.keys()))
            parent_paths    = deepcopy(list(parent_items.values()))
        elif isinstance(parent_items, list):
            parent_paths    = deepcopy(parent_items)
        else:
            raise TypeError(f'__inherit__ must be either dict or list: {parent_items}')

        ### check if any inherit paths are dictionaries
        ### and interpret them as mappings of platform-specific inherit paths
        platform_paths = list()
        for path in parent_paths:
            try:
                platform_paths.append(
                    platform.choose( path )
                    if isinstance( path, dict )
                    else path
                )
            except platform.MissingKeyError as e:
                log.info( term.red('Warning: '), f'{qualname(type(e))}( {e} )' )
        # log.info( term.blue( 'platform paths: ' ), platform_paths )

        ### attempt to resolve paths
        resolved_paths = list()
        with temporary_working_directory( self.path ) :
            for path in platform_paths:
                resolved_path = try_resolve( path, self.path )
                resolved_paths.append(resolved_path)

        ### evaluate tokens in resulting stringsa
        parsed_paths = ConfigSectionView( self.tree.root ).evaluate_list(
            '__inherit__',
            resolved_paths,
            kro=(self.tree.root,)
        )

        ### A node may not inherit itself
        if self.filepath in map(Path, parsed_paths):
            raise Config.InheritSelfError( str(self.filepath) )

        ### `with special_handling(parent_items):`
        if isinstance( parent_items, list ) : # todo: use context manager pattern here
            parent_aliases = deepcopy( parsed_paths )
        #
        # print('alias', parent_aliases)
        # print('paths', parsed_paths)
        # listprint(parsed_paths)
        result = OrderedDict( (k,v) for k,v in zip( parent_aliases, parsed_paths ) )

        ###
        return result

    class ParentsExtendError(Exception):
        ''' catch unknown exception while computing parents'''


    ####################
    @property
    def parents( self ) :
        ''' the full ordered set of all parent nodes, after recursive linearization'''

        # log.dinfo(term.green('parents '), self.filepath)
        parent_items    = self.__inherit__
        parents         = list()
        for parent_alias, parent_path in parent_items.items() :
            # log.dinfo(term.dgreen('parent '), parent_alias, term.dgreen(' | '), parent_path)

            parent      = self.tree[ Path(parent_path) ]
            parents.append( parent )

            parent_parents = parent.parents
            # log.info(term.cyan('__inherit__ '), parent_parents)

            ### Node A may not inherit Node B, if Node B inherits Node A
            if str(self.filepath) in parent_parents:
                raise Config.InheritLoopError(
                      '\n' + term.dcyan( 'Config:' ) + f' {str(self.filepath)}'
                    + '\n' + term.dcyan( 'Parent:' ) + f' {str(parent.filepath)}'
                    + ''   # raise Config.ParentNotfound
                )

            try:
                parents.extend( parent_parents )
            except Exception as e:
                raise Config.ParentsExtendError(e)
            # log.info(term.white('parents:', str(self.filename), parent_path ))

        result = GreedyOrderedSet( chain( parents, [self.tree.root] ) )
        # log.info(term.green('RESULT:'), list(p for p in result))
        return result


    ####################
    @property
    def parent_aliases( self ):
        alias_map = OrderedDict()
        for node in self.key_resolution_order:
            for alias, path in node.__inherit__.items():
                alias_map.setdefault(alias, path)

        # alias_map = ChainMap(list(map(lambda p: p.__inherit__, )))
        # for d in alias_map.maps:
        #     for key, value in d:
        #         if key in alias_map \
        #         and value != alias_map[key]:
        #             raise
        # print("alias_map", alias_map.items())
        return alias_map


    ####################
    @property
    def key_resolution_order( self ) :
        kro = GreedyOrderedSet( chain( [self], self.parents ) )
        # log.info('kro ', list(str(p) for p in kro))
        return kro


    #----------------------------------------------------------------#

    ####################
    def __getitem__( self, section_name ) :
        return ConfigSectionView( self, section_name )



    ####################
    def setdefault( self, key, default ) :
        ''' support for getdeepitem on Config object'''
        try :
            return self[key]
        except KeyError :
            return self._yaml_data.setdefault( key, default )


    ####################
    @property
    def sections( self ) :
        section_names = GreedyOrderedSet( )
        for node in self.key_resolution_order :
            for (key, section) in node.items( ) :
                if not key.startswith( '__' ) and not key.endswith( '__' ) :
                    section_names.add( key )
        return section_names

    def keys( self ) :
        kro = list( self.key_resolution_order )
        datalist    = [node._yaml_data for node in kro]
        datachain   = ChainMap( *datalist )
        keyview     = OrderedSet( sorted( datachain.keys( ) ) )
        return keyview


    ####################
    def items( self ) -> list :
        ''' unchained and unprocessed '''
        return self._yaml_data.items( )


    #----------------------------------------------------------------#

    ####################
    @property
    def __export__( self ):
        ''' parse the export dictionary for this node and return it'''

        # todo: BUG! why does 'pkg' or 'env' in the sections list evaluate to a path?
        try :
            export_items    = self['__export__'].items()
            parsed_dict     = export_items #OrderedDict()
            #parsed_paths    = ConfigSectionView( self.tree.root, '__export__' ).evaluate_list( '__exports__', export_dict )
            #todo: ConfigSectionView needs refactoring if it needs to be the entrypoint for this
            # print( term.green('PARSED~~~~~'), parsed_dict )
        except KeyError as e :
            parsed_dict = OrderedDict()

        # print( term.white( '_export' ), parsed_dict )
        return parsed_dict


    ####################
    @property
    def exports(self) -> OrderedDict:
        ''' a dictionary of exporter names mapped to a list of (output names, list of section keys)'''

        result = OrderedDict()
        result = OrderedDict()
        for node in self.key_resolution_order :
            #print( term.cyan( 'node:' ), node)
            for destination, speclist in node.__export__:
                parsed_destination = ConfigSectionView(self, PATH_VARS_SECTION).evaluate('__destination__', destination)
                assert len(speclist) > 1
                exporter_name   = speclist[0]
                export_subtrees = OrderedSet(speclist[1:])
                # print( term.white( '    export' ), destination, term.white('|'), exporter_name, term.white( '|' ), export_subtrees )

                if exporter_name not in result:
                    result[exporter_name] = OrderedDict()
                if parsed_destination not in result[exporter_name]:
                    result[exporter_name][parsed_destination] = export_subtrees
                else:
                    result[exporter_name][parsed_destination] |= export_subtrees

        return result

    #----------------------------------------------------------------#

    ScriptLine = namedtuple( 'CommandLine', ['command_word', 'args', 'kwargs'] )

    ####################
    @property
    def __script__( self ):
        ''' construct a flat yamlisp script data structure
            resolve the values of the config's script section
        '''
        raw_scripts = OrderedDict()
        with suppress(KeyError):
            raw_scripts = self._yaml_data['__script__']

        log.info('__script__')
        # rprint(raw_scripts)

        scripts = OrderedDict()
        for script_name, script_body in raw_scripts.items():
            scripts[script_name] = OrderedDict()
            # log.info('command_word: ', script_name)
            for line_name, s_expr in script_body.items():
                # log.info(f'    line: {line_name:<10} | {s_expr}')

                if line_name in scripts[script_name]:
                    raise Config.DuplicateScriptLineName(script_name, line_name )
                try:
                    command_word = s_expr[0]
                except IndexError as e:
                    raise Config.MissingCommandWordError(script_name, line_name, s_expr) from None

                command_args = list()
                with suppress(IndexError):
                    command_args = s_expr[1: ]

                args = list()
                kwargs = OrderedDict()
                for arg in command_args:
                    if isinstance(arg, dict):
                        for key, raw_value in arg.items():
                            if key in kwargs:
                                raise Config.YamlispKwargDuplicate(script_name, line_name, key)

                            value = self[PATH_VARS_SECTION].evaluate(key, raw_value, kro=self.key_resolution_order)
                            kwargs[key] = value
                    elif isinstance(arg, list):
                        value = self[PATH_VARS_SECTION].evaluate_list( '__script__', arg, kro=self.key_resolution_order )
                        args.append(value)
                    else:
                        value = self[PATH_VARS_SECTION].evaluate( '__script__', arg, kro=self.key_resolution_order )
                        args.append(value)

                scripts[script_name][line_name] = Config.ScriptLine( command_word, args, kwargs )

        rprint( scripts )

        return scripts




###

#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

class ConfigSectionView:
    ''' implement the multi chainmap key resolution algorithm on a config and its tree
        each instance of this class keeps track of a level of index depth in the value parsing algorithm
        dynamic chainmap - search config parents for keys if not found in the current one
        token expression substitution - evaluate to values from other keys, sections, and/or files
    '''

    ####################
    def __init__( self, config:Config, *names ) :
        self.config = config
        self.section_keys = names
        self.parse_counter = 0
        self.resultlist = list()


    ####################
    def __str__( self ) :
        return "".join( str( s ) for s in [
            '<', self.__class__.__name__, ': ', self.config.filepath, ' \'', self.section_keys, '\'>'
        ])

    __pprint__ = __str__
    __repr__ = str

    #----------------------------------------------------------------#

    ####################
    def keys( self ) :
        '''list of keys for the current subtree of the config'''

        key_union = GreedyOrderedSet()
        for key in getdeepitem( self.config._yaml_data, self.section_keys ).keys() :
            # print( term.green( 'key:' ), key )
            key_union.add( key )
        return list( key_union )

    def items( self ) :
        '''key-value tuples for the current subtree only, with values resolved'''

        # print( term.blue( 'items' ), self.section_keys )
        yield from map( lambda key : (
            key,
            getdeepitem( self.config, [*self.section_keys, key] )
        ),
                        self.keys()
                        )

    def values( self ) :
        for value in (p for k, p in self.items()) :
            yield value

    def paths( self ) :
        for path in map( Path, self.values() ) :
            yield path

    ####################
    class KeyValueTypeMismatch(Exception):
        ''' two parallel nodes did not have the same type for a key's value '''

    def allkeys( self ) :
        ''' get the union of keys for all nodes in the key resolution order '''

        key_union               = GreedyOrderedSet()
        key_sum                 = 0
        first_section_type      = None
        first_section           = None
        # if 'db' in self.section_keys:
        #     log.info(term.green('ALLKEYS DB '), self.config )

        for node in self.config.key_resolution_order :
            # print(term.cyan('node:'), node, self.section_keys, '\n',
            #       getdeepitem( node._yaml_data, self.section_keys ))
            try:
                section = getdeepitem( node._yaml_data, self.section_keys )
            except IndexError as e:
                continue

            if first_section_type is None:
                first_section_type  = type(section)
                first_section       = section
            elif first_section_type != type(section):
                raise ConfigSectionView.KeyValueTypeMismatch(self.config, self.section_keys, first_section, section)

            try :
                keys = section.keys()
            except AttributeError as e :
                keys = range( key_sum, key_sum+len( section ) )
                key_sum += len(keys)

            for key in keys :
                # print(term.green('    key:'), key)
                key_union.add( key )
        #     print( term.green( '\n------------------------------------' ))
        # print(term.cyan( '\n------------------------------------' ))
        # log.info('keys ', term.green(key_union))
        return list( key_union )

    def allitems( self ) :
        '''same as items, but uses allkeys method'''

        # print( term.blue( 'allitems' ), self.section_keys )
        yield from map(
            lambda key : (
                key,
                getdeepitem( self.config, [*self.section_keys, key], self.config.key_resolution_order )
            ),
            self.allkeys()
        )

    def allvalues( self ) :
        ''' full-depth values '''
        yield from (value for key, value in self.allitems())

    def allpaths( self ) :
        ''' full-depth values, convert values to Path objects before returning them '''
        yield from starmap( lambda k, v : (k, Path( v )), self.allitems() )


    #----------------------------------------------------------------#

    ####################
    def setdefault( self, key, default, kro ) :
        ''' support for getdeepitem on Config object'''
        # print( term.blue( "-----------------------------" ), 'begin setdefault', self.config, self.section_keys, term.white( key ) )
        try :
            return self._getitem(key, kro)
        except KeyError :
            return getdeepitem( self.config._yaml_data, self.section_keys, kro ).setdefault( key, default )
        # except ConfigSectionView.CouldNotGetItem as e:
        #     return None



    ###################
    def __getitem__( self, key ) :
        ''' obtain the 'flat' value of the key in the configtree, from the point of view of the current config
            if the current config contains the key, evaluate it and store it in a cache
            if the value is a list, evaluate each element of the list and return the parsed list
            if we need to look in a different node for the key, the process recurses from the point of view of that node
            paths are resolved relative to the path of the file they're defined in, so '.' means the current file's path.
            supports dictionaries inside dictionaries by returning nested ConfigSectionView objects
        '''
        # print(term.blue("-----------------------------"), 'begin __getitem__', self.config, term.white(key))
        return self._getitem(key, self.config.key_resolution_order)


    def _add2cache(self, key, value):
        raise NotImplementedError
        return getdeepitem( self.config._final_cache, self.section_keys )[key]


    ###################
    class CouldNotGetItem(Exception):
        ''' _getitem didn't find a result '''


    ###################
    def _getitem( self, key, kro) :

        ### check cache

        # try :
        #     # log.debug( self.config, term.red( ' | ' ), self.section_keys )
        #     final_value = getdeepitem( self.config._final_cache, self.section_keys )[key]
        # except KeyError :
        #     pass
        # except RecursionError:
        #     pass

        # except ConfigSectionView.CouldNotGetItem:
        #     pass
        # else:
            # print('else', self.config.name)
            # return final_value
        # if 'db' in self.section_keys:
        #     log.dinfo(term.dred('GETITEM'), self.config,term.dred(' | '), key, term.dred( ' | ' ), list(str(p) for p in kro))
        ### construct the current state of the inheritence chain
        if len(kro) == 0:
            pruned_kro = self.config.parents
        else:
            # print(term.red("PRUNE KRO"))
            # listprint(kro)
            pruned_kro = deque( kro )
            try:
                while pruned_kro.popleft( ) != self.config : pass
            except IndexError:
                pruned_kro = (self.config.tree.root,)
            # listprint(pruned_kro)
            # print( term.red( '--- pruned' ) )


        ### check current node
        # if 'db' in self.section_keys:
        #     log.info( term.pink( 'CHECK SELF ' ), self.config.filepath, ' keys ', self.section_keys, ' ', term.white( key ) )
        try:
            raw_value = getdeepitem( self.config._yaml_data, self.section_keys )[key]
        except KeyError:
            raw_value = None
        # except ConfigSectionView.CouldNotGetItem as e:
        #     pass
        else:
            if isinstance( raw_value, dict ) :                                                  # Dict Value Found
                # print( 'config_view', key )
                configview = ConfigSectionView( self.config, *self.section_keys, key )
                return configview

            elif isinstance( raw_value, list ) :                                                # List Value Found
                # log.info( 'list ', raw_value )
                try:
                    parsed_list = self.evaluate_list(key, raw_value, kro=pruned_kro)
                # except Config.SubstitutionValueTypeError as e: #todo: this works but hides a deeper structural error
                #     pass
                except: raise
                # print( term.cyan('~~~Cache List Result'), self.section_keys, key, self.config , parsed_list)
                #getdeepitem( self.config._final_cache, self.section_keys)[key] = parsed_list   # CACHE LIST ###
                else:
                    return parsed_list
                pass

            else :                                                                              # Scalar Value Found
                final_value = self.evaluate( key, raw_value , kro=pruned_kro)

                # print( term.cyan('~~~Cache Scalar Result'), self.section_keys, key, final_value )
                #getdeepitem( self.config._final_cache, self.section_keys )[key] = final_value   # CACHE VALUE ###
                return final_value


        ### check parents
        # if 'db' in self.section_keys:
        #     log.print(term.pink('CHECK PARENTS '), self.config.filepath, ' keys ', self.section_keys, term.white(key))
        #     print('parents')
        #     listprint(self.config.parents)
        #     print('kro')
        #     listprint(pruned_kro )
        for node in self.config.parents:
            # if 'db' in self.section_keys:
            #     log.info("look in parent: ", node)
            if node is self.config:
                continue
            try:
                parent_value = getdeepitem( node, self.section_keys, pruned_kro )._getitem( key, kro )
            except ConfigSectionView.CouldNotGetItem as e:
                continue
            # except Config.SubstitutionValueTypeError as e:
            #     continue
            else:
                # print(term.blue('parent_value:'), self.section_keys, key, parent_value, self.config.filepath)
                return parent_value

        for node in pruned_kro :
            # if key == 'db' :
            #     log.info( "look in kro: ", node )
            if node is self.config :
                continue
            try :
                parent_value = getdeepitem( node, self.section_keys, pruned_kro )._getitem( key, kro )
            except ConfigSectionView.CouldNotGetItem as e :
                continue
            # except Config.SubstitutionValueTypeError as e:
            #     continue
            else :
                return parent_value

        # not found
        # print('__getitem__', key, term.red('|'), self.config, term.red( '|' ),self.section_keys)
        raise ConfigSectionView.CouldNotGetItem( ''.join(str(s) for s in [
            '\nlookup:     ', str(self.config), '::',self.section_keys, ':', key,

            '\npruned kro: ', list( str( p ) for p in pruned_kro),
            '\nkro:        ', list( str( p ) for p in kro ),
            '\nparents:    ', self.config.parents
        ]))


    #----------------------------------------------------------------#

    #----------------------------------------------------------------#

    ####################
    def evaluate_list(self, key, raw_list, kro, scripts_data=None):
        ''' evaluate each element of the list, and return the list of parsed values '''
        parsed_list = []
        # print(term.yellow('------------'), 'EVALUATE LIST', raw_list)
        # listprint(kro)
        for (i, value) in enumerate( raw_list ) :
            if isinstance( value, list ) or isinstance( value, dict ) :
                new_value = ConfigSectionView( self.config, *self.section_keys, key, i )
            else :

                try:
                    # log.info('kro ', list(str(p) for p in kro))
                    new_value = self.evaluate( key, value, listeval=True, kro=kro, scripts_data=scripts_data )
                except ConfigSectionView.CouldNotGetItem as e:
                    if value[0] == '@':
                        continue
                    else:
                        raise
                # except Config.SubstitutionValueTypeError as e:
                #     parsed_list.extend(e.args[1])


                try :
                    resultlist = self.resultlist.pop( )
                    # print( "RESULTLIST:", resultlist )
                    parsed_list.extend(resultlist)
                    continue
                except IndexError as e :
                    pass

            parsed_list.append( new_value )
        return parsed_list


    ####################
    def evaluate(self, key, value, listeval=False, kro=(), scripts_data=None) -> str:
        ''' parse a raw value
            perform regex substitution on ${} token expressions until there are none left
            then attempt to resolve the result relative to the config file's path
        '''

        new_value=value
        total_count = 1
        # print(term.green('EVALUATE:'), key, value, self)

        while total_count > 0 :
            total_count = 0
            (new_value, count) = self.substitute(
                key,
                str(new_value),
                listeval=listeval,
                kro=kro,
                scripts_data=scripts_data
            )
            total_count += count

        with temporary_working_directory(self.config.path):
            final_value = try_resolve(new_value, self.config.path)

        return final_value  # todo: DifferedPath


    #----------------------------------------------------------------#

    ####################
    def substitute( self, key, value: str, listeval=False, kro=(), scripts_data=None ) :
        ''' responsible for running a single regex substitute
        '''
        total_count = 0
        count = None

        # log.debug( 'VALUE --- ', colored( value, 'red', attrs=['bold'] ) )
        expression_replacer = self.expression_parser( key, listeval=listeval, kro=kro, scripts_data=scripts_data)
        try:
            (result, count)     = token_expression_regex.subn( expression_replacer, value )

        # except Config.SubstitutionValueTypeError as e: # todo: handle this TypeError inside expression_replacer
        #     print(term.red('SUBSTITUTE'), key, value, self)
        #     raise e
        except RecursionError as e:
            raise RecursionError( self.config.filepath, self.section_keys, key, value) from None

        except Config.DelayedEvaluationTokenNotDuringScript as e:
            ### handle %-tokens
            count   = 0
            result  = e.args[0]
            # log.info('result: ', result)

        # log.debug( "After re.subn:  ", result, " | ", count, "|", expression_replacer.counter[0] )

        total_count += expression_replacer.counter[0] + count# ToDo: Replace monkey patch with class
        # log.debug( "Subn Result: ", result, ' after ',total_count )

        return result, total_count


    ####################
    class InvalidTokenReferenceToPreviousLine(Exception):
        ''' can't refer to the previous line on the first line of a script'''


    ####################
    def expression_parser( self, key, kro=(), listeval=False, scripts_data=None ) :
        ''' factory that creates a replace function to be used by regex subn
            process ${configpath::section:key} token expressions:
            -    key:        look up value in current section of current config
            -    sections:   [optional] look for key in a different section
            -    configpath: [optional] begin key lookup in a different node

            a token specifies a key that is to be looked up in a certain config node.
            If no section is specified, the same section the key is found in is searched.
            If no configpath is specified, the same file is assumed, except in the case of a self-referential key
            lookup for self-referential keys looks directly in the config's first parent.
            if configpath is specified, the parent list pseudo-chainmap behavior is still respected.
            if section or sections (section1:section2:section3) are specified, look in those sections
        '''

        counter = [0]

        def expression_replacer( matchobj ) :

            match       = matchobj.group(0)
            orig_value  = matchobj.string
            token       = matchobj.group('token')
            target_key  = matchobj.group('key')

            ### %-tokens are evaluated at run-time instead of compile-time
            ###     and use a different confipath::sections interpretation
            if token == '%' and scripts_data is None :
                raise Config.DelayedEvaluationTokenNotDuringScript( orig_value )
            elif token == '%' :
                ###
                if matchobj.group( 'configpath' ) is not None:
                    target_configpath = matchobj.group( 'configpath' )
                else:
                    target_configpath = scripts_data['current_script']
                ###
                if matchobj.group( 'sections' ) is not None:
                    target_sections = matchobj.group( 'sections' ).split( ':' )
                else:
                    target_sections = (scripts_data['previous_line'], )
                    if target_sections == (None, ):
                        raise Config.InvalidTokenReferenceToPreviousLine(target_configpath, target_sections, target_key)
                ###
                try :
                    line_results    = getattr(scripts_data['results'], str(target_configpath) )
                    result          = getattr(line_results, target_key)

                    return result
                except AttributeError as e :
                    raise Config.SubstitutionKeyNotFoundError( 'during script', target_configpath, target_sections, target_key, '\n' )

            ###################
            target_configpath = matchobj.group( 'configpath' ) \
                if (matchobj.group( 'configpath' ) is not None) \
                else self.config.filepath

            if target_configpath == 'ENV' :
                target_configpath = self.config.tree.env.filepath
            else:
                parents_aliases = self.config.parent_aliases
                if target_configpath in parents_aliases:
                    target_configpath = parents_aliases[target_configpath]

            ###################
            target_sections = matchobj.group( 'sections' ).split( ':' ) \
                if (matchobj.group( 'sections' ) is not None) \
                else self.section_keys

            # log.info( '>'*20, " MATCH ", target_configpath, ' ', target_sections, ' ', target_key, ' | ', key, ' ',  self.section_keys )
            # listprint(kro)
            # print("value", term.green(matchobj.group(0)))
            # print('-----------')

            # log.debug( matchobj.groups( ) )

            section_keys    = [*target_sections, target_key]
            node            = self.config.tree[target_configpath]

            ###################
            ### self-key references begin the search from the config's immediate parent
            if key == target_key \
            and self.section_keys == tuple(target_sections) \
            and self.config.filepath == target_configpath:
                node = kro[0]

            # if key == 'db':
            #     log.info(term.red('node '), node, ' | ', list(str(p) for p in kro),
            #              term.red('\nCould not find '), target_configpath, '::', target_sections, ':', target_key,
            #              term.red('\n for inserting into '), self.config.filepath, '::', self.section_keys, ':', key,
            #      )

            # try:
            result = getdeepitem(node, section_keys, kro)
            # except ConfigSectionView.CouldNotGetItem as e:
            #     raise RuntimeError(e)

            ###################
            # print(term.cyan("subn result:"), result, term.cyan('|'), key, term.cyan( '|' ), matchobj.group(0))
            if isinstance(result, OrderedDict) \
            and len(result) == 0:
                raise Config.SubstitutionKeyNotFoundError(''.join(str(s) for s in [
                    '\nCould not find ', target_configpath, '::', target_sections,':', target_key,
                    '\n for inserting into ', self.config.filepath, '::', self.section_keys,':', key,
                    '\n', kro
                ]))

            ###################
            elif isinstance(result, list) \
            and match == orig_value \
            and listeval \
            and token == '@':
                ### WARNING: use a hack to return a list out from the regex substitute
                ### so we can later use it to extend a list we're substituting into
                # log.info(term.blue('*'*30), 'LIST INSERT' )
                # todo: maybe use an exception to do this instead?
                self.resultlist.append(result)

            # elif result is None \
            # and match == orig_value \
            # and token == '@' :
            #     self.resultlist.append( list() )
            #
            # elif isinstance(result, ConfigSectionView)\
            #      and match == orig_value \
            #      and token == '@':
            #     log.info('rssult', result)
            #     self.resultlist.append( list() )

            ###################
            elif not isinstance(result, str):
                log.info( term.red( 'result ' ), result )
                log.info( term.red('result.keys() '), result.keys())
                log.info( term.red( 'result[0] ' ), result[0] )
                log.info( term.red( '@ ' ), match, ' | ', orig_value, ' | ', listeval, ' | ', token )
                raise Config.SubstitutionValueTypeError(
                    namedtuple('token', ['section', 'key', 'result'])
                            (target_sections, target_key, str(result)),
                    namedtuple( 'section', ['section', 'key', 'value'] )
                            (self.section_keys, key, matchobj.string),
                    )


            ###################
            elif token == '@':
                raise Config.TokenExpressionError('@ tokens may only be used to extend other sequences')

            ###################
            self.parse_counter += 1
            return str(result)

        ###
        expression_replacer.counter = counter

        return expression_replacer


#----------------------------------------------------------------------#

#todo: delayed key evaluation syntax -- causes a parent value to have its token expressions evaluated from the child's point of view
    # ^ this is achieved in part by using the ENV configpath keyword

token_expression_regex = re.compile(
    r"""(   (?P<token>[$@%])
          {                                     # ${
            ((?P<configpath>[^${}]+?)::)?       #   configpath@         [optional]
            ((?P<sections>[^${}]+):)?           #   sections:           [optional]
            #((?P<objects>[^${}]+).)?            #   objects.            [optional]
            (?P<key>[^$:{}]+?)                  #   key                 -required-
          })                                    #  }
    """, re.VERBOSE )


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

@export
class ConfigTree :
    """ container for a network of configuration files with chainmap-like behavior.
        config files may have other config files as parents.
        values may contain token expressions to be substituted with the value of a different key
        if only the key is specified, the same section and the same file are assumed
        if a section:key is not in the config file, look in the parents.
        all config files implicitly use the root node of the config filesystem as a parent.
        token expressions may refer to section:keys in any file in the configtree.
        ENV is a keyword that may be used as the filename for a token to refer to the current virtual environment's config
    """

    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    class NotFinalizedError(Exception):
        '''configtree should be finalized for writing before being used'''

    ####################
    def __init__( self, *
                  , root_file: Path = None
                  , env_path: Path = None
                  ) :

        self.nodes = OrderedDict( )
        self.root = None

        self.root_filepath = root_file
        self.env_filepath = env_path / self.envfile

        self.out_file = None
        self.raw_file = None
        self._final = False

        if root_file is not None :
            self.__add_root( root_file )


    ####################
    @classmethod
    def from_path( cls, target_path: Path ) :
        """ Find the root file for a target path, load it and its children. """

        ### Find Root File
        try:
            root_file = stack_of_files( target_path, '__root__.yml' )[0]
            root_path = root_file.parents[0]
        except IndexError as e:
            raise FileNotFoundError("Could not find '__root__.yml' file in <" +str(target_path)+ ">, or inside any parent directory")

        ### Find Env File
        try :
            env_file = stack_of_files( target_path, '__env__.yml' )[0]
            env_path = env_file.parents[0]
        except IndexError as e :
            log.info( 'Warning - __env__.yml file not found. Using root node...' )
            env_file = None
            env_path = root_file.parents[0]

        # print("env_file", env_path)
        self = cls( root_file=root_file, env_path=env_path )

        if env_file is not None:
            self.add_node(env_file)

        # todo: instead of searching for files, load files referenced by root and env, recursively
        # with temporary_working_directory( root_path ) :
        #     for file in find_yamls( root_path ) :
        #         if file != self.root.filepath :
        #             # todo: skip files that throw an invalid config exception
        #             self.add_node( Path( file ) )

        self.finalize()
        return self


    ####################
    @classmethod
    def from_root( cls, root_file: Path ) :
        self = cls( root_file=root_file )
        return self


    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    def add_root( self, root_file ) :
        assert self.root is None
        node = self.__add_node( root_file )
        self.root = node

    def add_node( self, target_file ) :
        try:
            assert target_file not in self.nodes
            node = Config.from_yaml( target_file, tree=self )
            self.nodes[node.filepath] = node
            return node
        except Config.EmptyFileWarning as e:
            log.debug( 'Config.EmptyFileWarning:', e )
        except Config.ProtocolError as e:
            log.debug( 'Config.ProtocolError:', e )
        except AssertionError as e:
            log.info( f'Node already exists {str(target_file)}' )

    def new_env(self, target_file):
        node                = self.add_node(target_file)
        self.env_filepath   = node.filepath


    __add_root  = add_root
    __add_node  = add_node
    __new_env   = new_env

    def finalize( self ) :
        self._final = True

    @property
    def final( self ) :
        return self._final


    #----------------------------------------------------------------#

    ####################
    def __getitem__( self, filepath=None ) :
        ''' return the config node at a given filepath
            if no filepath is given, return the root node
            if only a path is given, try to guess the filename
        '''
        if filepath is None :
            return self.root

        resolved_filepath = Path(filepath).resolve()

        with suppress( KeyError ) :
            return self.nodes[resolved_filepath]
        with suppress( KeyError ) :
            return self.nodes[resolved_filepath / '__env__.yml']
        with suppress( KeyError ) :
            return self.nodes[resolved_filepath / '__pkg__.yml']
        with suppress( KeyError ) :
            return self.nodes[resolved_filepath / '__root__.yml']

        raise KeyError( resolved_filepath, 'not found in', self )


    ####################
    def __len__( self ) :
        return len( self.nodes )

    ####################
    def __str__( self ) :
        return "".join( str( s ) for s in [
                '<', self.__class__.__name__, ' of ', self.root.__class__.__name__,
                ': [', len( self ), '], root=', self.root.path if self.root is not None else 'None', '>'
            ] )

    __pprint__ = __str__
    __repr__ = str


    #----------------------------------------------------------------#

    @property
    def envfile( self ) :
        return '__env__.yml'

    ####################
    def find_nodes( self, pattern ) :
        results = list( )
        for (node_filepath, node) in self.nodes.items( ) :
            if re.match( pattern, str( node.filename ) ) is not None :
                results.append( node )
        if len( results ) == 0 :
            results.append( self.root )
        return results

    @property
    def envlist( self ) :
        return self.find_nodes( self.envfile )

    @property
    def packagelist( self ) :
        return self.find_nodes( '__pkg__\.yml' )

    ####################
    @property
    def by_name( self ) :
        result = defaultdict( list )
        for (name, node) in self.nodes.items( ) :
            result[node.filename.split( '.' )[0]].append( node )
        return result

    @property
    def by_env( self ) :
        result = dict( )
        for node in self.envlist :
            result.setdefault( node.path.name, node )
        return result

    @property
    def by_pkg( self ) :
        result = dict( )
        for node in self.packagelist :
            result.setdefault( node.path.name, node )
        return result

    def node( self, name=None ) :
        if name is None :
            return self.nodes[self.env_filepath ]
        return self.nodes[name]


    @property
    def env( self ) -> Config :
        try :
            return self.nodes[self.env_filepath ]
        except KeyError as e :
            log.debug( 'KeyError:', e )
            return self.root


    #----------------------------------------------------------------#

    def nearest_node( self, target_name: str, target_path: Path ) :
        """ return the child config node for the nearest parent of the target path."""
        # Todo: perform this on the saved config structure, not the filesystem.
        for filepath in stack_of_files( target_path, target_name ) :
            if filepath in self.nodes.keys( ) :
                return filepath



#----------------------------------------------------------------------#

add_pprint( ConfigTree )
add_pprint( Config )


#----------------------------------------------------------------------#

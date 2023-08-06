#-- smash.core.yamlisp

"""
yamlisp script execution
"""

#todo: separate out the yaml processing from the core config concepts; configtree should be a metaclass representing configs as classes

from powertools import AutoLogger
log = AutoLogger()
from powertools import term
from powertools.print import listprint, dictprint, rprint, pprint, pformat, add_pprint
from powertools import GreedyOrderedSet
from powertools import qualname

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

from ..util.yaml import load as load_yaml
from ..util.path import stack_of_files
from ..util.path import temporary_working_directory
from ..util.path import try_resolve
from ..util.path import find_yamls



#----------------------------------------------------------------------#

from .config import Config
from .env import Environment
from .plugins import tools


class MissingScriptError( Exception ) :
    ''' attempting to execute a command word not found in the config file'''

class SubcommandNotFound( Exception ) :
    ''' could not find a tool or script to handle a line'''

####################
def run_yamlisp(    env: Environment,
                    config: Config,
                    command_word:   str,
                    g_args:         list,
                    g_kwargs:       dict,
                    *,
                    scripts_results=None,
                ):
    ''' execute a command word from a yamlisp file '''

    ### get the script data structure and select our command word
    scripts = config.__script__
    # dictprint(scripts)
    try :
        script = scripts[command_word]
    except KeyError :
        raise MissingScriptError( command_word ) from None

    scripts_data = OrderedDict()
    scripts_data['current_script'] = command_word
    scripts_data['current_line'] = list( script.items() )[0]
    scripts_data['previous_line'] = None
    if scripts_results is None:
        scripts_results = OrderedDict()
        for script_name in scripts:
            scripts_results[script_name] = OrderedDict()
    else:
        scripts_data['results'] = scripts=scripts_results

    ### execute command-word, line-by-line
    for line_name, (subcommand, args, kwargs) in script.items() :
        log.print('')
        log.info(f'run_line: {line_name}'
                 f', {subcommand}, {args}, {kwargs}')
        result = None

        ### run a command-word defined in the same file (!!!DANGER!!!)
        # todo: don't do this...
        if subcommand in scripts:
            result = run_yamlisp(
                env, config, subcommand,
                scripts_results   = scripts_results,
                g_args            = args,
                g_kwargs          = g_kwargs
            )

        ### run a registered Tool subclass
        elif subcommand in tools:
            tool = tools[subcommand]
            log.info('tool ', tool)

            args.extend( g_args )
            kwargs.update( g_kwargs )
            result = tool( env, config ).run( *args, **kwargs )

        ###
        else:
            raise SubcommandNotFound( line_name ) from None

        scripts_results[command_word][line_name] = result

    ###
    return scripts_results


###

#----------------------------------------------------------------------#


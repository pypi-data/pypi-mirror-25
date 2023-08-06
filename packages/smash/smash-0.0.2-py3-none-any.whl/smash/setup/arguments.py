#-- smash.setup.arguments

'''--- Smart Shell
    An integrated environment for reproducible research, development, testing, and production
'''

#----------------------------------------------------------------------#

from pathlib import Path
import os
from pprint import pprint

def collect_package_data( package_path ) :
    root_path = Path( __file__ ).parents[2].resolve() / package_path
    package_data = list()

    for root, _, _ in os.walk( str( root_path ) ) :
        package_data.append( str( Path( root ) / '*' ) )

    return package_data


#----------------------------------------------------------------------#

kwargs = dict(
    name            = 'smash',
    version         = '0.0.2',
    description     = __doc__,

    url             = 'https://github.com/philipov/smash',
    author          = 'Philip Loguinov',
    author_email    = 'philipov@gmail.com',

    packages = [
        'smash',            # main application

        'smash.core',       # fundamental abstractions
        'smash.tool',       # extensive subapplications
        'smash.util',       # low-level utilities
        'smash.setup',      # arguments for setup.py
        'smash.templates',   # library of default files

        'smash.boot',       # instance manager
        'smash.pkg',        # package manager
        'smash.env',        # environment manager
        'smash.test',       # testing manager
        'smash.dash',       # graphical user interface

    ],

    zip_safe                = True,
    include_package_data    = True,
    package_data = {
        'smash.templates' : collect_package_data( Path('smash')/'templates' )
    },
    entry_points = {
        'console_scripts': [
            'smash      = smash:console',
            'smash.boot = smash.boot:console',
            'smash.env  = smash.env:console',
            'smash.pkg  = smash.pkg:console',
            'smash.git  = smash.git:console',
            'smash.test = smash.test:console',
        ],
    },
    install_requires = [
        'powertools',       # std lib extension
        'psutil',           # process utils
        'ruamel.yaml',      # yaml parser
        'xmltodict',        # xml parser
        'ordered_set',      # ...

        'click',            # command-line parser
        'cookiecutter',     # filesystem templater
        'conda',            # package manager
        'dulwich',          # git
        'wget',             # downloader

        'colored_traceback',
        'colorama',
        'termcolor',
    ],


    classifiers = [
        'Environment :: Console',
        'Environment :: Other Environment',

        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Customer Service',

        'License :: Other/Proprietary License',

        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.6'
    ]
)

from copy import deepcopy
test_kwargs = deepcopy( kwargs )
test_kwargs['install_requires'].append( 'pytest' )

dev_kwargs = deepcopy( test_kwargs )

__version__ = kwargs['version']

#----------------------------------------------------------------------#

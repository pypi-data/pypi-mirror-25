#-- smash.__init__

"""--- Smart Shell
An integrated environment for reproducible research and development: from idea to production.
"""

from smash.setup.arguments import __version__

from .__main__ import console


from .core.config import Config
from .core.config import ConfigSectionView
from .core.config import ConfigTree


from .core.env import *
from .core.instance import *
from .core.pkg import *

from .core.exporter import *
from .core.handler import *
from .core.tool import *
from .core.user import *

# from .core import plugins

from .core.plugins import environment_types
from .core.plugins import instance_templates
from .core.plugins import package_types
from .core.plugins import packages
from .core.plugins import tools
from .core.plugins import exporters
from .core.plugins import handlers

from .core import platform


#----------------------------------------------------------------------#


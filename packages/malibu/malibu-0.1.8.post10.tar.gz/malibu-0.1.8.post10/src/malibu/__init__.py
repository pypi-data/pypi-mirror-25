# -*- coding: utf-8 -*-
from malibu import command  # noqa
from malibu import config  # noqa
from malibu import database  # noqa
from malibu import design  # noqa
from malibu import text  # noqa
from malibu import util  # noqa

import subprocess

__git_label__ = ''
try:
    __git_label__ = subprocess.check_output(
        [
            'git',
            'rev-parse',
            '--short',
            'HEAD'
        ],
        stderr=subprocess.PIPE
    )
    __git_label__ = __git_label__.decode('utf-8').strip()
except (subprocess.CalledProcessError, AttributeError, IOError):
    __git_label__ = 'RELEASE'

__version__ = '0.1.8-10'
__release__ = '{}-{}'.format(__version__, __git_label__)
__doc__ = """
malibu is a collection of classes and utilities that make writing code
a little bit easier and a little less tedious.

The whole point of this library is to have a small codebase that could
be easily reused across projects with nice, easily loadable chunks that
can be used disjointly.
"""

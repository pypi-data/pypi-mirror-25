# -*- coding: utf-8 -*-
"""
notifierlib package

Imports all parts from notifierlib here
"""
from ._version import __version__
from notifierlib import Notifier, Group
from channels.email import Email
from channels.stdout import Stdout

__author__ = '''Costas Tyfoxylos'''
__email__ = '''costas.tyf@gmail.com'''
__version__ = __version__

# This is to 'use' the module(s), so lint doesn't complain
assert __version__


# assert objects
assert Notifier
assert Group


# assert channels
assert Email
assert Stdout

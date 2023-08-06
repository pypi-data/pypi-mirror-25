# -*- coding: utf-8 -*-
"""
certbotlib package

Imports all parts from certbotlib here
"""
from ._version import __version__
from .certbotlib import Certbot

__author__ = '''Oriol Fabregas'''
__email__ = '''oriol.fabregas@payconiq.com'''

# This is to 'use' the module(s), so lint doesn't complain
assert __version__
assert Certbot

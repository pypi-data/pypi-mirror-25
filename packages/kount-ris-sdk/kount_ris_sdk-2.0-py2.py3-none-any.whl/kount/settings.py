#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"settings"
from __future__ import absolute_import, unicode_literals, division, print_function
from kount.version import VERSION


__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

PYTHON_VERSION = "3.6.1"
RESOURCE_FOLDER = "resources"
XML_FILENAME = 'validate.xml'
XML_DICT = 'xml_rules.py'
SDK_VERSION = "0695"

#~ raise errors or log them, excl. "ValueError: Configured configurationKey is incorrect."
#~ RAISE_ERRORS = False
RAISE_ERRORS = True


# request's timeout
TIMEOUT = 5

#~ fake configuration key, replace with the valid one orovided by Kount
configurationKey = b"<+oue+DGm>F(&p)Ch4`2AU&;>AoD]4FCfN8Bl7Q+E-62?Df]K2/c"

#~ uncomment this if you'd like to get the configurationKey from the environment
#~ import os
#~ try:
    #~ configurationKey = os.environ['K_KEY']
#~ except KeyError:
    #~ print("The default fake configurationKey set. Required actual one from Kount")

#~ put configurationKey in the local_settings.py and don't commit it
#~ comment this code if the configurationKey is an environment variable
try:
    from .local_settings import *
except ImportError as ie:
    print("The default fake configurationKey set. Required actual one from Kount. ", ie)

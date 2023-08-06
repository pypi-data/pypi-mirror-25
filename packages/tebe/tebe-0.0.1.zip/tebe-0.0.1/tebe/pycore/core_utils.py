# -*- coding: utf-8 -*-
'''
Extra module used for code refactoring.
This is a temporary container for procedures, classes etc.
that are moved from other modules during code refactoring.
If needed they should be refactored and should be moved
to more suitable module or class.
'''

import os
import re

import mistune

def abspath(relpath=None):
    _this_dir = os.path.dirname(os.path.abspath(__file__))
    _loge_dir = os.path.split(_this_dir)[0]
    if relpath:
        return os.path.join(_loge_dir, relpath)
    else:
        return _loge_dir
        
APP_PATH = abspath()

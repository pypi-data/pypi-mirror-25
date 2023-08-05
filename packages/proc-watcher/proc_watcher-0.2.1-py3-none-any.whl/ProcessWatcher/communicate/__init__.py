# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
config file from 
'/usr/local'+' /etc/process-watcher/watcher.conf'

the section name is your index of key value
'''
import sys
import os


def get_config_file():
    default_path = os.path.join(sys.prefix, 'etc/process-watcher/watcher.conf')
    if not os.path.exists(default_path):
        default_path = os.path.join(sys.prefix, 'local', 'etc/process-watcher/watcher.conf')
    if not os.path.exists(default_path):
        print(default_path + 'not exists!\n', file=sys.stderr)
    return default_path

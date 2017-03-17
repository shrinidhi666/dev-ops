#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import requests

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import lib.constants
import lib.config
import lib.processor
import lib.slave_utils
import socket
import simplejson

r = requests.get("http://devops:"+ str(lib.config.slave_conf['master_rest_port']) +"/download/test.deb")
lib.debug.debug(r.content)

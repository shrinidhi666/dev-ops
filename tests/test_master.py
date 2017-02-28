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

hostname =  socket.gethostname()
ip = socket.gethostbyname(hostname)
testdata = lib.slave_utils.slaveconst().slaveconst()
testdata['wtf'] = 'wtf1'
r = requests.post("http://devops:"+ str(lib.config.slave_conf['master_rest_port']) +"/states/"+ hostname +"/files/firefox/1",data=simplejson.dumps(testdata))
lib.debug.debug(r.content)
try:
  work = simplejson.loads(r.content)
  for x in work:
    lib.debug.debug(x)
except:
  lib.debug.error(sys.exc_info())


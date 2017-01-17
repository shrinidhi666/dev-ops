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
testdata['wtf'] = 'wtf'
testdata['punk'] = 'punk'
r = requests.post("http://devops:"+ str(lib.config.master_port) +"/states/"+ hostname +"/level1.level2.level3_1",json=simplejson.dumps(testdata))
work = simplejson.loads(r.content)
lib.debug.info(work)
for x in work:
  lib.processor.process(x)

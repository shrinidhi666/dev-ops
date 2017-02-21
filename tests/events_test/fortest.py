#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import time
import simplejson

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))


def test(data):
  time.sleep(10)
  f = open("/tmp/testing.event","w")
  f.write(simplejson.dumps(data))
  f.flush()
  f.close()
  return ("this is tesing test")

def forblue(data):
  f = open("/tmp/testing.event_forblue", "w")
  f.write(simplejson.dumps(data))
  f.flush()
  f.close()
  print(data)
  return ("this is tesing forblue1")




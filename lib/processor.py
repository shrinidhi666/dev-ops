#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.template
import lib.transport
import lib.debug
import lib.modules
import simplejson

def process(kwargs):
  for x in kwargs.keys():
    lib.debug.debug(x)
    for y in kwargs[x].keys():
      module_to_load = "lib.modules.{0}".format(unicode(y).strip())
      module_to_load_args = []
      lib.debug.debug("\_ {0}".format(y))
      for z in kwargs[x][y].keys():
        key = unicode(z).strip()
        if(type(kwargs[x][y][z]) == str):
          value = '\''+ unicode(kwargs[x][y][z]) +'\''
        else:
          value = unicode(kwargs[x][y][z])
        module_to_load_args.append("{0}={1}".format(key,value))
        lib.debug.debug("\t\_ {0} : {1}".format(key,value))
      module_final_run = "cmd_ret = "+ module_to_load +"("+ ",".join(module_to_load_args) +")"
      lib.debug.info(module_final_run)
      try:
        exec(module_final_run)
        for x in cmd_ret:
          lib.debug.info("{0} : {1}".format(x,cmd_ret[x]))
      except:
        lib.debug.warning(sys.exc_info())


  # lib.debug.info(simplejson.dumps(kwargs))


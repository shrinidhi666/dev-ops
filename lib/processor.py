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
import lib.config
import requests
import lib.constants

def process(request_id,state_name,kwargs):
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
      lib.debug.debug(module_final_run)
      try:
        exec(module_final_run)
        for w in cmd_ret:
          lib.debug.debug("{0} : {1}".format(w,cmd_ret[w]))
          to_rest = {}
          to_rest[request_id] = {lib.constants.hostname :{state_name :{x :{y :{w : cmd_ret[w]}}}}}
          r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/slaves/return/result", data=simplejson.dumps(to_rest))
          lib.debug.debug(r.content)
      except:
        to_rest = {}
        to_rest[request_id] = {lib.constants.hostname: {state_name: {x: {y: [str(sys.exc_info()),1]}}}}
        lib.debug.warning(sys.exc_info())


  # lib.debug.info(simplejson.dumps(kwargs))


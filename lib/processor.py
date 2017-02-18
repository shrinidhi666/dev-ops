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
import lib.slave_utils

def process(request_id,state_name,kwargs,is_local = False,dry_run = False):
  for x in kwargs.keys():
    lib.debug.debug(x)
    slaveconst = lib.slave_utils.slaveconst().slaveconst()
    event_start = None
    event_end = None
    event_result = None
    event_data = {}
    event = None
    module_loaded = False
    if (kwargs[x].has_key("event.fire")):
      event = kwargs[x]['event.fire']
      event_data['state'] = {}
      event_data['state']['name'] = state_name
      event_data['state']['detail'] = {x: kwargs[x]}
      event_data['request_id'] = request_id
      if (event.has_key("start")):
        event_start = event['start']
      if (event.has_key("end")):
        event_end = event['end']
      if (event.has_key("result")):
        event_result = event['result']


    for y in kwargs[x].keys():
      if(y == "event.fire"):
        continue
      module_loaded = True
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
        if(event_start):
          event_data['id'] = event_start
          slaveconst['event'] = event_data
          r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/event", data=simplejson.dumps(slaveconst))
          r_content = r.content
          lib.debug.debug(r_content)

        exec(module_final_run)

        if (event_end):
          event_data['id'] = event_end
          slaveconst['event'] = event_data
          r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/event", data=simplejson.dumps(slaveconst))
          r_content = r.content
          lib.debug.debug(r_content)

        lib.debug.debug(cmd_ret)

        if (event_result):
          event_data['id'] = event_result
          event_data['result'] = cmd_ret
          slaveconst['event'] = event_data
          r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/event", data=simplejson.dumps(slaveconst))
          r_content = r.content
          lib.debug.debug(r_content)

        for w in cmd_ret:
          lib.debug.debug("{0} : {1}".format(w,cmd_ret[w]))
          to_rest = {}
          to_rest[request_id] = {lib.constants.hostname :{state_name :{x :{y :{w : cmd_ret[w]}}}}}
          if(is_local):
            print(simplejson.dumps(to_rest,indent=4))
          else:
            r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/slaves/return/result", data=simplejson.dumps(to_rest))
            r_content = r.content
            lib.debug.debug(r_content)
          # if(cmd_ret[w][-1] != 0):
          #   return(0)
      except:
        to_rest = {}
        to_rest[request_id] = {lib.constants.hostname: {state_name: {x: {y: [str(sys.exc_info()),1]}}}}
        if(is_local):
          print(simplejson.dumps(to_rest,indent=4))
        else:
          r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/slaves/return/result", data=simplejson.dumps(to_rest))
          r_content = r.content
          lib.debug.debug(r_content)
        lib.debug.error(sys.exc_info())
        return(0)

    if(not module_loaded):
      if (event_start):
        event_data['id'] = event_start
        slaveconst['event'] = event_data
        r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/event", data=simplejson.dumps(slaveconst))
        r_content = r.content
        lib.debug.debug(r_content)

      if (event_end):
        event_data['id'] = event_end
        slaveconst['event'] = event_data
        r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/event", data=simplejson.dumps(slaveconst))
        r_content = r.content
        lib.debug.debug(r_content)


  return(1)


  # lib.debug.info(simplejson.dumps(kwargs))


#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.transport
import lib.constants
import lib.modules
import lib.debug
import lib.config
import lib.slave_utils
import lib.processor
import simplejson
import requests
import multiprocessing





class slave_sub(lib.transport.subscriber):

  def process(self, topic, request_id,state_name):
    slaveconst = lib.slave_utils.slaveconst().slaveconst()
    r = requests.post("http://"+ lib.config.slave_conf['master'] +":"+ str(lib.config.slave_conf['master_rest_port']) + "/states/" + lib.constants.hostname + "/"+ state_name , data=simplejson.dumps(slaveconst))
    work = simplejson.loads(r.content)
    if(work):
      for x in work:
        lib.debug.debug(x)
        lib.processor.process(request_id,state_name,x)


def register_host():
  slavedata = {}
  slavedata['hostid'] = lib.slave_utils.hostid()
  slavedata['hostname'] = lib.constants.hostname
  slavedata['ip'] = lib.constants.ip

  lib.debug.info(slavedata)
  r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/slaves/register",data=simplejson.dumps(slavedata))
  lib.debug.info(r.content)


def start_sub(q=None):

  sub = slave_sub(topic=[lib.constants.hostname,lib.constants.ip])


if __name__ == '__main__':
  qu = multiprocessing.Queue()
  register_host()
  start_sub()



    









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
import simplejson
import requests
import multiprocessing
import socket
import platform




class slave_sub(lib.transport.subscriber):
  def process(self, topic, request_id,state_name):
    slaveconst = lib.slave_utils.slaveconst().slaveconst()
    r = requests.post("http://"+ lib.config.slave_conf['master'] +":"+ str(lib.config.master_port) + "/states/" + lib.constants.hostname + "/"+ state_name , json=simplejson.dumps(testdata))
    work = simplejson.loads(r.content)
    lib.debug.info(work)
    for x in work:
      lib.processor.process(x)


def register_host():
  slavedata = {}
  slavedata['hostid'] = lib.slave_utils.hostid()
  slavedata['hostname'] = lib.constants.hostname
  slavedata['ip'] = lib.constants.ip

  lib.debug.info(slavedata)
  r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.master_port) + "/register",json=simplejson.dumps(slavedata))
  lib.debug.info(r.content)


def main():

  sub = slave_sub(topic=[lib.constants.hostname])


if __name__ == '__main__':
  register_host()



    









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
import tempfile
import signal
import psutil
import fcntl
import time

app_lock_file = os.path.join(tempfile.gettempdir(),"devops-slave.lock")

def receive_signal(signum, stack):
  quit()

signal.signal(signal.SIGTERM, receive_signal)
signal.signal(signal.SIGINT, receive_signal)
signal.signal(signal.SIGABRT, receive_signal)
signal.signal(signal.SIGHUP, receive_signal)
signal.signal(signal.SIGSEGV, receive_signal)

def quit():
  try:
    os.remove(app_lock_file)
  except:
    lib.debug.error(sys.exc_info())
  sys.exit(0)


def app_lock():
  import random
  time.sleep(random.uniform(0.000,0.500))
  if(os.path.exists(app_lock_file)):
    f = open(app_lock_file,"r")
    pid = f.read().strip()
    f.close()
    try:
      p = psutil.Process(int(pid))
      lib.debug.info(p.cmdline()[1])
      if(os.path.abspath(p.cmdline()[1]) == os.path.abspath(__file__)):
        lib.debug.warning("already an instance of the app is running.")
        lib.debug.warning("delete the file {0}".format(app_lock_file))
        os._exit(1)
      else:
        raise Exception("seems like a different process has the same pid")
    except:
      lib.debug.warn(sys.exc_info())
      f = open(app_lock_file,"w")
      try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
      except:
        lib.debug.error(sys.exc_info())
        os._exit(1)
      f.write(unicode(os.getpid()))
      f.flush()
      fcntl.flock(f, fcntl.LOCK_UN)
      f.close()
  else:
    f = open(app_lock_file,"w")
    try:
      fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
      lib.debug.error(sys.exc_info())
      os._exit(1)
    f.write(unicode(os.getpid()))
    f.flush()
    fcntl.flock(f, fcntl.LOCK_UN)
    f.close()



class slave_sub(lib.transport.subscriber):

  def process(self, topic, request_id,state_name):
    slaveconst = lib.slave_utils.slaveconst().slaveconst()
    r = requests.post("http://"+ lib.config.slave_conf['master'] +":"+ str(lib.config.slave_conf['master_rest_port']) + "/states/" + lib.constants.hostname + "/"+ state_name +"/0" , data=simplejson.dumps(slaveconst))
    print(r.content)
    work = simplejson.loads(r.content)
    if(work):
      for x in work:
        lib.debug.debug(x)
        done = lib.processor.process(request_id,state_name,x)
        if(not done):
          return(0)
    return(1)


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
  app_lock()
  register_host()
  start_sub()



    









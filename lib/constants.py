#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.debug
import appdirs
import os
import sqlite3
import socket
import tempfile
import requests

# DO NOT PUT ANYTHING THATS SUPPOSED TO BE IN A CONFIG FILE HERE
# IE: NOTHING SHOULD BE HERE THAT GENERATED DYNAMICALLY.

os.environ['XDG_CONFIG_DIRS'] = '/etc'
configdir = os.path.join(appdirs.site_config_dir(),"dev-ops")
masterdir = os.path.join(configdir,"master")
slavedir = os.path.join(configdir,"slave")
default_delimiter = "__"
m_private_key_file = os.path.join(masterdir, "private_key.pem")
s_private_key_file = os.path.join(slavedir, "private_key.pem")
m_config_file = os.path.join(masterdir, "master.conf")
s_config_file = os.path.join(slavedir, "slave.conf")
m_keys_sqlite3_file = os.path.join(masterdir, "sqlite", "keys.sqlite3")
m_dostates_sqlite3_file = os.path.join(masterdir, "sqlite", "do-states.sqlite3")
s_slaveconst_dir = os.path.join(slavedir, "slaveconst")
s_backup_dir = os.path.join(slavedir, "backup")
hostname = socket.gethostname()
while(True):
  try:
    ip = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/getmyip").content
    break
  except:
    lib.debug.info(sys.exc_info())

m_result_logs_dir = tempfile.gettempdir()
m_result_logs_prefix = "devops.result"
m_result_logs_prefix_hosts = "devops.hosts"
m_result_logs_delimiter = default_delimiter
s_process_lock_file = os.path.join(tempfile.gettempdir(),"devops.slave.process.lock")



class pub_q__status():
  pending = 0
  recieved = 1
  started = 2
  running = 3
  done = 4
  failed = 5
  killed = 6

class slaves_status():
  pending = 0
  accepted = 1
  rejected = 2

  def __getitem__(self, item):
    a = {}
    a[0] = "pending"
    a[1] = "accepted"
    a[2] = "rejected"
    return(a[item])

class tasktypes():
  key_register = "key.register"
  cmd_run = "cmd.run"
  file_sync = "file.sync"
  host_register = "host.register"
  rule_get = "rule.get"

class msg_keys():
  tasktype = "tasktype"
  hostname = "hostname"
  id = "id"
  payload = "payload"





if __name__ == '__main__':
  lib.debug.warn(slaves_status()[slaves_status.accepted])
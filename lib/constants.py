#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import appdirs
import os
import sqlite3



os.environ['XDG_CONFIG_DIRS'] = '/etc'
configdir = os.path.join(appdirs.site_config_dir(),"dev_ops")
private_key_file = os.path.join(configdir,"private_key.pem")
master_config_file = os.path.join(configdir,"master.conf")
slave_config_file = os.path.join(configdir,"slave.conf")

class pub_q__status():
  pending = 0
  recieved = 1
  started = 2
  running = 3
  done = 4
  failed = 5
  killed = 6

class keys__status():
  pending = 0
  accepted = 1

class tasktypes():
  key_register = "register"
  cmd_run = "cmd.run"
  file_sync = "file.sync"

class msg_keys():
  tasktype = "tasktype"
  hostname = "hostname"
  id = "id"
  payload = "payload"






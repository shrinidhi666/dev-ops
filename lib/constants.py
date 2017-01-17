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


# DO NOT PUT ANYTHING THATS SUPPOSED TO BE IN A CONFIG FILE HERE
# IE: NOTHING SHOULD BE HERE THAT GENERATED DYNAMICALLY.

os.environ['XDG_CONFIG_DIRS'] = '/etc'
configdir = os.path.join(appdirs.site_config_dir(),"dev_ops")
masterdir = os.path.join(configdir,"master")
slavedir = os.path.join(configdir,"slave")
master_private_key_file = os.path.join(masterdir, "private_key.pem")
slave_private_key_file = os.path.join(slavedir, "private_key.pem")
master_config_file = os.path.join(masterdir,"master.conf")
slave_config_file = os.path.join(slavedir,"slave.conf")
master_sqlite3_file = os.path.join(masterdir,"sqlite","master.sqlite3")
slave_slaveconst_dir = os.path.join(slavedir,"slaveconst")
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


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






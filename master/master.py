#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.transport
import lib.constants
import lib.db_sqlite3
import simplejson

class master(lib.transport.server):

  def process(self, msg):
    msgdict = eval(msg)
    if(msgdict[lib.constants.msg_keys.tasktype] == lib.constants.tasktypes.key_register):

      conn = lib.db_sqlite3.db.connect()
      rows = conn.execute("select * from pub_q")
      print (rows.fetchall())


if(__name__ == "__main__"):
  master().start()
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
import lib.debug
import simplejson

class master(lib.transport.server):

  def process(self, message, message_type=None):
    # msgdict = eval(msg)
    # lib.debug.info(message)
    # return (msg)
    if(message_type == lib.constants.tasktypes.host_register):
      msgdict = simplejson.loads(message)
      lib.debug.info(msgdict)
      conn = lib.db_sqlite3.db.connect()
      rows = conn.execute("insert into slaves")
      # print (msgdict[lib.constants.msg_keys.payload])
    return(message)


if(__name__ == "__main__"):
  a = master()
  a.start(pool_size=1)
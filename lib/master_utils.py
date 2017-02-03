#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
import fnmatch
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.db_sqlite3
import lib.constants
import lib.debug


def get_slaves(status=None):
  if(status):
    if(status == lib.constants.slaves_status.pending):
      data = lib.db_sqlite3.execute("select * from slaves where status="+ lib.constants.slaves_status.pending,dictionary=True)
    elif(status == lib.constants.slaves_status.accepted):
      data = lib.db_sqlite3.execute("select * from slaves where status=" + lib.constants.slaves_status.accepted,dictionary=True)
    else:
      data = lib.db_sqlite3.execute("select * from slaves where status=" + lib.constants.slaves_status.rejected,dictionary=True)
  else:
    data = lib.db_sqlite3.execute("select * from slaves",dictionary=True)
  return(data)


def get_slaves_match(match):
  matched_data = []
  try:
    data = lib.db_sqlite3.execute("select * from slaves where status="+ str(lib.constants.slaves_status.accepted),dictionary=True)
  except:
    lib.debug.error(str(sys.exc_info()))
  if(data):
    for x in data:
      # lib.debug.debug(x)
      if(fnmatch.fnmatch(x['hostname'],match) or fnmatch.fnmatch(x['ip'],match)):
        matched_data.append(x)

  return(matched_data)



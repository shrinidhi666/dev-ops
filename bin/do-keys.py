#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
import argparse
import fnmatch

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import lib.constants
import lib.config
import lib.db_sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("-l","--list",dest="list",action="store_true",help="list all the keys")
parser.add_argument("-a","--accept",dest="accept",help="accept comma seperated keys")
parser.add_argument("-r","--reject",dest="reject",help="reject comma seperated keys")
parser.add_argument("-d","--delete",dest="delete",help="delete comma seperated keys")
args = parser.parse_args()

if(args.list):
  conn = lib.db_sqlite3.db.connect()
  rows = conn.execute("select * from slaves")
  data = rows.fetchall()
  for x in data:
    if(x):
      print(x['hostname'] +" : "+ x['ip'] +" : "+ lib.constants.slaves_status()[int(x['status'])])
else:
  if(args.accept):
    if(args.accept == "all"):
      try:
        lib.db_sqlite3.execute("update slaves set status=\""+ str(lib.constants.slaves_status.accepted) +"\" where status=\""+ str(lib.constants.slaves_status.pending) +"\"")
      except:
        print(sys.exc_info())
    else:
      accept_list = args.accept.split(",")
      print(accept_list)
      for x in accept_list:
        try:
          lib.db_sqlite3.execute("update slaves set status=\""+ str(lib.constants.slaves_status.accepted) +"\" where ip=\""+ x +"\" or hostname=\""+ x +"\"")
        except:
          print(sys.exc_info())

  if (args.reject):
    accept_list = args.reject.split(",")
    print(accept_list)
    for x in accept_list:
      try:
        lib.db_sqlite3.execute("update slaves set status=\"" + str(lib.constants.slaves_status.rejected) + "\" where ip=\"" + x + "\" or hostname=\"" + x + "\"")
      except:
        print(sys.exc_info())

  if (args.delete):
    accept_list = args.reject.split(",")
    print(accept_list)
    for x in accept_list:
      try:
        lib.db_sqlite3.execute("delete from slaves where ip=\"" + x + "\" or hostname=\"" + x + "\"")
      except:
        print(sys.exc_info())



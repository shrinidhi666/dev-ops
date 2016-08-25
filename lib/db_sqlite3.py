#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import sqlite3



module_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
print("module path = {0}".format(module_path))

class db(object):

  @staticmethod
  def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
    return d

  @staticmethod
  def connect():
    global module_path
    db_file = os.path.join(module_path,"data","db","sqlite","master.sqlite3")
    print (db_file)
    try:
      conn = sqlite3.connect(db_file)
      conn.isolation_level = None
      conn.row_factory = db.dict_factory
    except:
      print (sys.exc_info())
      return (0)
    return (conn)


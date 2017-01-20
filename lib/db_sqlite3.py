#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.constants
import lib.debug
import sqlite3



class db(object):

  @staticmethod
  def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
    return d

  @staticmethod
  def connect():
    db_file = lib.constants.master_sqlite3_file
    lib.debug.debug("connecting to sqlite file :"+ db_file)
    try:
      conn = sqlite3.connect(db_file)
      conn.isolation_level = None
      conn.row_factory = db.dict_factory
    except:
      print (sys.exc_info())
      return (0)
    return (conn)


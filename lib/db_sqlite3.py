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
  def connect(db_file=None):
    """
    connect to a sqlite3 database.
    :param db_file: if not specified then use the master sqlite file
    :return: connection object
    """
    if(not db_file):
      db_file = lib.constants.m_keys_sqlite3_file
    lib.debug.debug("connecting to sqlite file :"+ db_file)
    try:
      conn = sqlite3.connect(db_file,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
      conn.isolation_level = None
      conn.row_factory = db.dict_factory
    except:
      print (sys.exc_info())
      return (0)
    return (conn)


def execute(query,dictionary=False,db_file=None):
  con = db.connect(db_file=db_file)
  if(con):
    if(dictionary):
      try:
        rows = con.execute(query)
        data = rows.fetchall()
      except:
        lib.debug.error(str(sys.exc_info()))
        try:
          con.close()
        except:
          lib.debug.error(str(sys.exc_info()))
        raise

      try:
        con.close()
      except:
        lib.debug.error(str(sys.exc_info()))
      if(not isinstance(data,int)):
        return(data)
      else:
        return(0)
    else:
      try:
        con.execute(query)
      except:
        lib.debug.error(str(sys.exc_info()))
        try:
          con.close()
        except:
          lib.debug.error(str(sys.exc_info()))
        raise

      try:
        con.close()
      except:
        lib.debug.error(str(sys.exc_info()))
      return(1)
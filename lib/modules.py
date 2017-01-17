#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import lib.db_sqlite3
import subprocess

class cmd(object):

  @staticmethod
  def run(command=[],user=None,path=None,shell=True,log=True,env=None):
    """

    :param self:
    :param command:
    :param user:
    :param path:
    :param shell:
    :param log:
    :param env: dict of environment variables to set
    :return: (msg, errorcode)
    """
    returner = {}
    cwd = os.getcwd()

    if(path):
      os.chdir(path)
    for cmd in command:
      lib.debug.info("running : {0}".format(cmd))
      try:
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell,cwd=path,universal_newlines=True,env=env)
        returner[cmd] = (p.communicate(), p.returncode)
      except:
        returner[cmd] = (sys.exc_info(), 1)
    if(path):
      os.chdir(cwd)
    return (returner)



class host(object):

  @staticmethod
  def register(hostdetails):
    """

    :param hostdetails:
    :return:
    """
    try:
      conn = lib.db_sqlite3.db.connect()
      conn.execute("insert into slaves (ip, hostname) values (\"{0}\",\"{1}\")".format(hostdetails['ip'], hostdetails['hostname']))
      conn.close()
      return(1)
    except:
      lib.debug.error(sys.exc_info())
      try:
        conn.close()
      except:
        lib.debug.warn(sys.exc_info())
      return(0)

class file(object):

  @staticmethod
  def sync(user=None,group=None,mode=None,source=None,backup=True):
    pass



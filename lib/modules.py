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
import simplejson

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
    :return: ([msg, errorcode])

    ALL MODULES SHOULD RETURN LIST WITH -1 INDEX AS THE RETURN CODE : 0 -> SUCCESS else FAIL
    """
    returner = {}
    cwd = os.getcwd()

    if(path):
      os.chdir(path)
    for cmd in command:
      lib.debug.info("running : {0}".format(cmd))
      try:
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell,cwd=path,universal_newlines=True,env=env)
        (stdout, stderr) = p.communicate()
        returner[cmd] = [(stdout,stderr), p.returncode]
      except:
        returner[cmd] = [unicode(sys.exc_info()), 1]
        break
    if(path):
      os.chdir(cwd)
    return (returner)



class file(object):

  @staticmethod
  def sync(user=None,group=None,mode=None,source=str,dest=None,backup=True):
    if(source.startswith("devops://")):
      pass





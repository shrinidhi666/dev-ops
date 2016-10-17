#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import subprocess

class cmd(object):

  @staticmethod
  def run(self,command,user=None,path=None,shell=True,log=True,env=None):
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
    try:
      p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell,cwd=path,universal_newlines=True,env=env)
      return(p.communicate()[0],p.returncode)
    except:
      return(sys.exc_info(),1)


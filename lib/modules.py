#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import lib.slave_utils
import lib.db_sqlite3
import lib.config
import lib.constants
import subprocess
import simplejson
import requests
import shutil
import time
try:
  import pwd
  import grp
except:
  lib.debug.error(sys.exc_info())
class cmd(object):

  @staticmethod
  def run(command=[],user=None,group=None,path=None,shell=True,log=True,env=None):
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
    if(env):
      os.environ.update(env)
    if(path):
      os.chdir(path)
    for cmd in command:
      lib.debug.info("running : {0}".format(cmd))
      try:
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell)
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
  def sync(user=None,group=None,mode=None,source=None,dest=None,backup=True,template=True):
    returner = {}
    lib.debug.debug(source)
    if(source):
      if(source.startswith("devops://")):
        try:
          slaveconst = lib.slave_utils.slaveconst().slaveconst()

          source_dry = str(source).replace("devops://","")
          slaveconst['file.sync'] = source_dry
          r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/filesync", data=simplejson.dumps(slaveconst))
          file_data = r.content
          if(backup):
            if(os.path.exists(dest)):
              try:
                os.makedirs(lib.constants.s_backup_dir)
              except:
                lib.debug.debug(sys.exc_info())
              lib.debug.debug("backup : "+ os.path.join(lib.constants.s_backup_dir, dest.split(os.sep)[-1] + lib.constants.default_delimiter + str(time.time())))
              shutil.copy(dest,os.path.join(lib.constants.s_backup_dir, dest.split(os.sep)[-1] + lib.constants.default_delimiter + str(time.time())))
          fd = open(dest,"w")
          fd.write(file_data)
          fd.flush()
          fd.close()
          if(mode):
            os.chmod(dest,mode)
          if(user and group):
            os.chown(dest,pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)
          returner[dest] = ["file updated",0]
          return(returner)
        except:
          returner[dest] = [unicode(sys.exc_info()), 1]
          return(returner)




#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import argparse
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))
import lib.constants
import lib.debug
import subprocess


supervisorpath = "/etc/supervisor/conf.d/"
installdir = "/opt/dev-ops"
progpath = installdir
source_master_path = os.path.join(progpath,"install","master")
source_slave_path = os.path.join(progpath,"install","slave")
slave_supervisorconf = os.path.join(progpath,"install","supervisor","slave")
master_supervisorconf = os.path.join(progpath,"install","supervisor","master")
lib.debug.info(progpath)

parser = argparse.ArgumentParser()
parser.add_argument("--slave",dest="slave",action="store_true",help="install config files for slave")
parser.add_argument("--master",dest="master",action="store_true",help="install config files for master")
args = parser.parse_args()


gitclone = "cd /opt/ ; git clone https://github.com/shrinidhi666/dev-ops.git ;cd /opt/dev-ops; git checkout master; cd -"
gitpull =  "cd /opt/dev-opts ; git pull ; cd -"

def gitupdate():
  p = subprocess.Popen(gitpull,shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  output = p.communicate()
  print (output)
  ret = p.wait()
  return(ret)

def gitnew():
  p = subprocess.Popen(gitclone,shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  output = p.communicate()
  print (output)
  ret = p.wait()
  return(ret)


if(args.master):
  if(os.path.exists(installdir)):
    ret = gitupdate()
  else:
    ret = gitnew()

  if(ret):
    sys.exit(1)


  try:
    os.makedirs(lib.constants.masterdir)
  except:
    lib.debug.warn(sys.exc_info())

  try:
    os.system("rsync -av "+ source_master_path.rstrip(os.sep) +"/ "+ lib.constants.masterdir.rstrip(os.sep) +"/")
  except:
    lib.debug.warn(sys.exc_info())


if(args.slave):
  if (os.path.exists(installdir)):
    ret = gitupdate()
  else:
    ret = gitnew()

  if (ret):
    sys.exit(1)

  try:
    os.makedirs(lib.constants.slavedir)
  except:
    lib.debug.warn(sys.exc_info())

  try:
    os.system("rsync -av "+ source_slave_path.rstrip(os.sep) +"/ "+ lib.constants.slavedir.rstrip(os.sep) +"/")
  except:
    lib.debug.warn(sys.exc_info())





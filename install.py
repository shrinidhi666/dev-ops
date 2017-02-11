#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import argparse
import subprocess
import appdirs


os.environ['XDG_CONFIG_DIRS'] = '/etc'
configdir = os.path.join(appdirs.site_config_dir(),"dev_ops")
masterdir = os.path.join(configdir,"master")
slavedir = os.path.join(configdir,"slave")


supervisorpath = "/etc/supervisor/conf.d/"
installdir = "/opt/dev-ops"
states_path = "/srv/devops/states/"
progpath = installdir
source_master_path = os.path.join(progpath,"install","master")
source_slave_path = os.path.join(progpath,"install","slave")
slave_supervisorconf = os.path.join(progpath,"install","supervisor","slave")
master_supervisorconf = os.path.join(progpath,"install","supervisor","master")
print(progpath)

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
    os.makedirs(masterdir)
  except:
    print(sys.exc_info())


  try:
    os.makedirs(states_path)
  except:
    print(sys.exc_info())


  try:
    os.system("rsync -av "+ source_master_path.rstrip(os.sep) +"/ "+ masterdir.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())

  try:
    os.system("rsync -av "+ master_supervisorconf.rstrip(os.sep) +"/ "+ supervisorpath.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())


if(args.slave):
  if (os.path.exists(installdir)):
    ret = gitupdate()
  else:
    ret = gitnew()

  if (ret):
    sys.exit(1)

  try:
    os.makedirs(slavedir)
  except:
    print(sys.exc_info())

  try:
    os.system("rsync -av "+ source_slave_path.rstrip(os.sep) +"/ "+ slavedir.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())

  try:
    os.system("rsync -av "+ slave_supervisorconf.rstrip(os.sep) +"/ "+ supervisorpath.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())





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


progpath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
source_master_path = os.path.join(progpath,"install","master")
source_slave_path = os.path.join(progpath,"install","slave")
lib.debug.info(progpath)

parser = argparse.ArgumentParser()
parser.add_argument("--slave",dest="slave",action="store_true",help="install config files for slave")
parser.add_argument("--master",dest="master",action="store_true",help="install config files for master")
args = parser.parse_args()

if(args.master):
  try:
    os.makedirs(lib.constants.masterdir)
  except:
    lib.debug.warn(sys.exc_info())

  try:
    os.system("rsync -av "+ source_master_path.rstrip(os.sep) +"/ "+ lib.constants.masterdir.rstrip(os.sep) +"/")
  except:
    lib.debug.warn(sys.exc_info())


if(args.slave):
  try:
    os.makedirs(lib.constants.slavedir)
  except:
    lib.debug.warn(sys.exc_info())

  try:
    os.system("rsync -av "+ source_slave_path.rstrip(os.sep) +"/ "+ lib.constants.slavedir.rstrip(os.sep) +"/")
  except:
    lib.debug.warn(sys.exc_info())





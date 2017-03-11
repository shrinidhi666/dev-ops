#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.debug
import lib.constants
import yaml
import glob

if(os.path.exists(lib.constants.s_config_file)):
  slave_fd = open(lib.constants.s_config_file, "r")
  slave_conf = yaml.safe_load(slave_fd)
  # lib.debug.info("slave conf : ")
  # lib.debug.info(slave_conf)

if(os.path.exists(lib.constants.m_config_file)):
  master_fd = open(lib.constants.m_config_file, "r")
  master_conf = yaml.safe_load(master_fd)
  # lib.debug.info("master conf : ")
  # lib.debug.info(master_conf)


# try:
#   master_port = master_conf['master_rest_port']
# except:
#   lib.debug.warn("master.conf file doesnt have the option for master_rest_port")
#   try:
#     master_port = slave_conf['master_rest_port']
#   except:
#     lib.debug.warn("slave.conf file doesnt have the option for master_rest_port")
#     master_port = 9491
#
#
#


#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.constants
import yaml

if(os.path.exists(lib.constants.s_config_file)):
  __slave_fd = open(lib.constants.s_config_file, "r")
  slave_conf = yaml.safe_load(__slave_fd)
  __slave_fd.close()

if(os.path.exists(lib.constants.m_config_file)):
  __master_fd = open(lib.constants.m_config_file, "r")
  master_conf = yaml.safe_load(__master_fd)
  __master_fd.close()

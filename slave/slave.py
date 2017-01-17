#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.transport
import lib.constants
import lib.modules
import lib.debug
import lib.config
import lib.slave_utils
import simplejson
import requests
import multiprocessing
import socket
import platform




class slave_sub(lib.transport.subscriber):
  def process(self, topic, request_id,state_name):
    slaveconst = lib.slave_utils.slaveconst().slaveconst()




    









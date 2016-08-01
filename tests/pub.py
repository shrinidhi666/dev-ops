#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import random
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.core
import time

pub = lib.core.publisher()

while(True):
  topic = random.randint(1,10)
  pub.publish(topic,{'test':'wtf'})
  time.sleep(0.5)


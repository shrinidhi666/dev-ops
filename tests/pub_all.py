#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import random
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.transport
import time

pub = lib.transport.publisher()
topic = "all"
pub.publish(2, {'test': 'x'})
time.sleep(0.5)
for x in range(0,10):
  print (x)
  pub.publish(topic, {'test': x})
  time.sleep(0.5)

for x in range(0, 10):
  print (x)
  pub.publish(topic, {'test': x})
  time.sleep(0.5)
  # time.sleep(0.5)
# while(True):
#   topic = 2
#   pub.publish(topic,{'test':topic})
#   time.sleep(0.5)


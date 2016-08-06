#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.template

if(__name__ == "__main__"):
  test = lib.template.root()
  test_state = lib.template.states()
  print (test.list)
  print (test_state.list)
  print (test_state.render("level1.level2.test1"))
  print (test_state.render("level1.level2.level3.test1"))
  print ("____")
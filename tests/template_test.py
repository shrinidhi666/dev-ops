#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.template
import lib.processor

env1 = {}
env2 = {}
env1["test"] = "we are mad"
env2["wtf"] = False

env1["u"] = "testing strings"
slaveconst = {}
slaveconst.update(env2)
slaveconst.update(env1)

if(__name__ == "__main__"):
  # test = lib.template.root()
  test_state = lib.template.states()
  rendered_file = test_state.render("jinjafile.jinja",slaveconst=slaveconst,is_file=True)
  try:
    rendered_state = test_state.render("level1.level2.level3")
  except:
    print (sys.exc_info())
    sys.exit(1)
  print(rendered_file)
  print (rendered_state)
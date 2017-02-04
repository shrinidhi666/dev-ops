#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import jinja2

file_to_load = sys.argv[1]

env1 = {}
env2 = {}
env1["test"] = "we are mad"
env2["wtf"] = False

env1["u"] = "testing strings"

fd = open(file_to_load,"r")
file_contents = fd.read()
fd.close()

template = jinja2.Template(file_contents)
file_contents = None
file_rendered = template.render(env1=env1,env2=env2)
print(file_rendered)
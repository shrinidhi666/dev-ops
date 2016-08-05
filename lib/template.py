#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import jinja2
import yaml


class load():
  def __init__(self,path="./"):
    self._path = path



  def get(self):
    loader = jinja2.FileSystemLoader(self._path)
    return(loader.list_templates())


class load_state(load):


  def get(self):
    loader = jinja2.FileSystemLoader(self._path)
    j2_env = Environment(loader=loader, trim_blocks=True)
    ret_loader = []
    for x in loader.list_templates():
      if(unicode(x).endswith('.yml')):
        print (x)
        ret_loader.append(x)

    return (ret_loader)

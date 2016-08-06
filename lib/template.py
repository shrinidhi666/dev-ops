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


# def list_dirs(startpath):
#   ret_dirs = [startpath]
#   for root, dirs, files in os.walk(startpath):
#     for dir in dirs:
#       ret_dirs.append(os.path.abspath(os.path.join(root,dir)))
#   print (ret_dirs)
#   return(ret_dirs)


class root(object):
  def __init__(self,path="./"):
    self._path = os.path.abspath(path)
    self._loader = None
    self._env = None




  @property
  def list(self):
    self._loader = jinja2.FileSystemLoader(self._path)
    self._env = jinja2.Environment(loader=self._loader, trim_blocks=True)
    return(self._loader.list_templates())

  @list.setter
  def list(self,value):
    pass

  def render(self,path):
    pass


class states(root):

  @property
  def list(self):
    self._loader = jinja2.FileSystemLoader(self._path)
    self._env = jinja2.Environment(loader=self._loader, trim_blocks=True)
    ret_loader = {}
    for x in self._loader.list_templates():
      if(unicode(x).endswith('.yml')):
        ret_loader[((unicode(x).rstrip('.yml')).replace("/","."))] = unicode(x)
    return (ret_loader)

  def render(self,state_path):
    template_file = self.list[state_path]
    template_env = self._env.get_template(template_file)
    yml_content = template_env.render()
    print (yaml.load(yml_content))



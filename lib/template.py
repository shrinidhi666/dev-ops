#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug

import jinja2
import yaml
import copy


# def list_dirs(startpath):
#   ret_dirs = [startpath]
#   for root, dirs, files in os.walk(startpath):
#     for dir in dirs:
#       ret_dirs.append(os.path.abspath(os.path.join(root,dir)))
#   print (ret_dirs)
#   return(ret_dirs)


class root(object):
  def __init__(self, path="./"):
    self._path = os.path.abspath(path)


  @property
  def list(self):
    return (self._loader.list_templates())

  @property
  def _loader(self):
    return jinja2.FileSystemLoader(self._path)

  @_loader.setter
  def _loader(self,value):
    pass

  @property
  def _env(self):
    return jinja2.Environment(loader=self._loader, trim_blocks=True)


  @_env.setter
  def _env(self,value):
    pass


  @list.setter
  def list(self, value):
    pass

  def render(self, path):
    pass


class states(root):
  @property
  def list(self):
    """
    get a list of all the state files in the directory tree

    :return:
     dictionary
    """
    # self._loader = jinja2.FileSystemLoader(self._path)
    # self._env = jinja2.Environment(loader=self._loader, trim_blocks=True)
    ret_loader = {}
    for x in self._loader.list_templates():
      if (unicode(x).endswith('.yml')):
        if (unicode(x).split("/")[-1] == "init.yml"):
          ret_loader[unicode(x).rstrip('/init.yml').replace("/", ".")] = unicode(x)
        else:
          ret_loader[unicode(x).rstrip('.yml').replace("/", ".")] = unicode(x)
    return (ret_loader)

  def render(self, path, slaveconst={}, masterconst={}, is_file=False,cyclic_test={}):
    if (is_file):
      template_env = self._env.get_template(path)
      filecontent = template_env.render(slaveconst=slaveconst, masterconst=masterconst)
      return (filecontent)
    if (self.list.has_key(path)):
      template_file = self.list[path]
      if (cyclic_test.has_key(template_file)):
        raise Exception("cyclic redundancy : " + str(template_file))
      cyclic_test[template_file] = 1
      template_env = self._env.get_template(template_file)
      # lib.debug.info(slaveconst)
      yml_content = template_env.render(slaveconst=slaveconst, masterconst=masterconst)
      yml_objs = yaml.safe_load(yml_content)
      return_obj = []
      if (template_file.split("/")[-1] == "init.yml"):
        for yml_obj in yml_objs:
          retured_obj = self.render(yml_obj, slaveconst=slaveconst, masterconst=masterconst)
          if (retured_obj):
            return_obj.extend(retured_obj)
      else:
        if (isinstance(yml_objs, dict)):
          return_obj.append(yml_objs)
        else:
          return_obj = yml_objs
      return (return_obj)
    else:
      return (None)

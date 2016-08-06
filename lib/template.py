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
    """
    get a list of all the state files in the directory tree

    :return:
     dictionary
    """
    self._loader = jinja2.FileSystemLoader(self._path)
    self._env = jinja2.Environment(loader=self._loader, trim_blocks=True)
    ret_loader = {}
    for x in self._loader.list_templates():
      if(unicode(x).endswith('.yml')):
        if(unicode(x).split("/")[-1] == "init.yml"):
          ret_loader[unicode(x).rstrip('/init.yml').replace("/",".")] = unicode(x)
        else:
          ret_loader[unicode(x).rstrip('.yml').replace("/",".")] = unicode(x)
    return (ret_loader)

  def render(self,state_path):
    template_file = self.list[state_path]
    template_env = self._env.get_template(template_file)
    yml_content = template_env.render()
    yml_objs = yaml.load(yml_content)
    return_obj = []
    if(template_file.split("/")[-1] == "init.yml"):
      for yml_obj in yml_objs:
        ret = self.render(yml_obj)
        # temp_file = self.list[yml_obj]
        # temp_env = self._env.get_template(temp_file)
        # temp_content = temp_env.render()
        return_obj.append(ret)
    else:
      if(isinstance(yml_objs,dict)):
        return_obj.append(yml_objs)
      else:
        return_obj = yml_objs
    return (return_obj)



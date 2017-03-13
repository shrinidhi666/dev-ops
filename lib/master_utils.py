#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
import fnmatch
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.db_sqlite3
import lib.constants
import lib.debug
import lib.template
import lib.config
import collections
import yaml


def get_slaves(status=None):
  if(status):
    if(status == lib.constants.slaves_status.pending):
      data = lib.db_sqlite3.execute("select * from slaves where status="+ lib.constants.slaves_status.pending,dictionary=True)
    elif(status == lib.constants.slaves_status.accepted):
      data = lib.db_sqlite3.execute("select * from slaves where status=" + lib.constants.slaves_status.accepted,dictionary=True)
    else:
      data = lib.db_sqlite3.execute("select * from slaves where status=" + lib.constants.slaves_status.rejected,dictionary=True)
  else:
    data = lib.db_sqlite3.execute("select * from slaves",dictionary=True)
  return(data)


def get_slaves_match(match):
  matched_data = []
  try:
    data = lib.db_sqlite3.execute("select * from slaves where status="+ str(lib.constants.slaves_status.accepted),dictionary=True)
  except:
    lib.debug.error(str(sys.exc_info()))
  if(data):
    for x in data:
      # lib.debug.debug(x)
      if(fnmatch.fnmatch(x['hostname'],match) or fnmatch.fnmatch(x['ip'],match) or fnmatch.fnmatch(x['hostid'],match)):
        matched_data.append(x)

  return(matched_data)



def event_handler(data):
  even_root = lib.config.master_conf['events_root']
  # even_root = "/home/shrinidhi/bin/gitHub/dev-ops/tests/events_test"
  event_templates = lib.template.states(path=even_root) #lib.config.master_conf['events_root']
  event_high = event_templates.render("high",slaveconst=data)
  lib.debug.debug(event_high)
  lib.debug.debug("got event : "+ data['event']['id'])
  try:
    sys.path.index(even_root)
  except:
    sys.path.append(even_root)
  if(event_high):
    for x in event_high:
      if(x.has_key(data['event']['id'])):
        for event in x:
          lib.debug.debug(x[event])
          for event_key in x[event]:
            # if(sys.modules.has_key(x[event][event_key]['import'])):
            #   mod_import = "reload("+ x[event][event_key]['import'] +")"
            # else:
            mod_import = "import " + x[event][event_key]['import']
            mod_run = "mod_ret = "+ x[event][event_key]['run'] + "(data)"
            exec mod_import
            lib.debug.debug("importing : "+ str(sys.modules[x[event][event_key]['import']].__file__))
            exec mod_run
            lib.debug.debug(mod_import +" : "+ mod_run)
            lib.debug.debug(mod_ret)




def render_high(high_state_obj,slaveconst={},masterconst={}):
  valid_states_list = []
  for hs in high_state_obj:
    for fn_exp in hs.keys():
      (const_key, const_exp) = (fn_exp.split(":")[:-1], fn_exp.split(":")[-1])
      states_list = hs[fn_exp]['states']
      if(hs[fn_exp].has_key("match")):
        match = hs[fn_exp]["match"]

        if(match == "slaveconst"):
          formatch = slaveconst
          for sc in const_key:
            formatch = formatch[sc]

          if(hs[fn_exp].has_key("compare")):
            comp_obj = hs[fn_exp]['compare']
            if(isinstance(comp_obj,dict)):
              comp_op = comp_obj['operator']
              comp_type = comp_obj['type']
              comp_str = "is_match = True if(" + comp_type +"(formatch) "+ comp_op +" "+ comp_type +"(const_exp)) else False"
              lib.debug.debug(comp_str)
              exec comp_str
              if(is_match):
                lib.debug.debug("matched : " + unicode(formatch) + " : " + unicode(const_exp))
                valid_states_list.extend(states_list)
            else:
              return("compare object is not a dict : "+ str(comp_obj))
          else:
            if(fnmatch.fnmatch(unicode(formatch),unicode(const_exp))):
              lib.debug.debug("matched : "+ unicode(formatch) +" : "+ unicode(const_exp))
              valid_states_list.extend(states_list)
          # lib.debug.debug(str(const_key) + " : " + str(const_exp) + " : " + str(formatch))
        elif(match == "cidr"):
          ipset = netaddr.IPSet(netaddr.IPNetwork(const_key))
          if(slaveconst['ip'] in ipset):
            valid_states_list.extend(states_list)
        else:
          return("match should be either cidr or slaveconst")
      else:
        lib.debug.debug(fn_exp)
        validhosts = lib.master_utils.get_slaves_match(fn_exp)
        lib.debug.debug(validhosts)
        if((slaveconst['ip'] in [x['ip'] for x in validhosts])):
          lib.debug.debug("found valid host : "+ str(slaveconst['hostname']))
          valid_states_list.extend(states_list)

  dupcheck = collections.OrderedDict()
  if(valid_states_list):
    for x in valid_states_list:
      dupcheck[x] = 1
  valid_states_list = [x for x in dupcheck.keys()]

  return(valid_states_list)


class masterconst(lib.template.states):

  def __init__(self, path=None):
    if(path):
      self._path = os.path.abspath(path)
    else:
      self._path = lib.config.master_conf['masterconst_root']

  def masterconst(self,slaveconst={}):
    state_list = None
    if(self.list.has_key("high")):
      highobj = self.render("high",slaveconst=slaveconst)

      valid_states = render_high(highobj,slaveconst=slaveconst)
      lib.debug.debug(valid_states)
      if(valid_states):
        state_list = valid_states
      else:
        state_list = self.list
    else:
      state_list = self.list
    const_dict = {}
    for x in state_list:
      if(x == "high"):
        continue
      if(not self.list.has_key(x)):
        lib.debug.debug("No state named : "+ str(x))
        continue
      template_file = self.list[x]

      template_env = self._env.get_template(template_file)
      yml_content = template_env.render(slaveconst=slaveconst)
      yml_objs = yaml.safe_load(yml_content)
      if(isinstance(yml_objs,dict)):
        for yo in yml_objs:
          if (const_dict.has_key(yo)):
            lib.debug.warn("duplicate key : "+ str(yo) +" : "+ template_file)
        const_dict.update(yml_objs)
      elif(isinstance(yml_objs,list)):
        for yml_obj in yml_objs:
          if(isinstance(yml_obj,dict)):
            for yo in yml_obj:
              if(const_dict.has_key(yo)):
                lib.debug.warn("duplicate key : "+ str(yo) +" : "+ template_file)
              const_dict[yo] = yml_obj[yo]
          else:
            if(const_dict.has_key(yml_obj)):
              lib.debug.warn("duplicate key : " + str(yml_obj) +" : "+ template_file)
            const_dict[yml_obj] = True
        # lib.debug.debug(yml_objs)
    lib.debug.debug(const_dict)



if __name__ == '__main__':
  mc = masterconst(path="/home/shrinidhi/bin/gitHub/dev-ops/tests/master_const")
  mc.masterconst()


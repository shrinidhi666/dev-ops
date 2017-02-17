#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import flask

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.template
import lib.constants
import lib.db_sqlite3
import lib.modules
import lib.debug
import simplejson
import lib.config
import lib.master_utils
import time
import fnmatch
import collections



app = flask.Flask(__name__)

@app.route('/states/<hostid>/<state>/<isfile>',methods=['POST'])
def states(hostid,state,isfile):
  slaveconst = simplejson.loads(flask.request.data)
  all_states = lib.template.states(path="../tests/states_test")
  lib.debug.debug(hostid)
  lib.debug.debug(state)
  lib.debug.debug(isfile)
  lib.debug.debug(slaveconst)
  if(int(isfile)):
    try:
      ret_state_details = all_states.render(unicode(state), slaveconst=slaveconst,is_file=True)
    except:
      return (unicode(sys.exc_info()))
    return unicode(ret_state_details)
  else:
    ret_state_details = all_states.render(unicode(state), slaveconst=slaveconst)
    return simplejson.dumps(ret_state_details)


@app.route('/high/<hostid>',methods=['POST'])
def high(hostid):
  slaveconst = simplejson.loads(flask.request.data)
  all_states = lib.template.states(path="../tests/states_test")
  lib.debug.debug(slaveconst)
  high_state_obj = all_states.render("high", slaveconst=slaveconst)
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
          ipset = netaddr.IPSet(netaddr.IPNetwork("192.168.1.0/29"))
          if(slaveconst['ip'] in ipset):
            valid_states_list.extend(states_list)
        else:
          return("match should be either cidr or slaveconst")
      else:
        lib.debug.debug(fn_exp)
        validhosts = lib.master_utils.get_slaves_match(fn_exp)
        lib.debug.debug(validhosts)
        if((slaveconst['ip'] in [x['ip'] for x in validhosts])):
          lib.debug.debug("found valid host")
          valid_states_list.extend(states_list)

  dupcheck = collections.OrderedDict()
  if(valid_states_list):
    for x in valid_states_list:
      dupcheck[x] = 1
  valid_states_list = [x for x in dupcheck.keys()]

  state_contents = []
  for x in valid_states_list:
    state_x_content = all_states.render(x,slaveconst=slaveconst)
    if(state_x_content):
      state_contents.extend(state_x_content)


  lib.debug.debug(state_contents)
  return simplejson.dumps(state_contents)


@app.route('/states/list',methods=['GET'])
def states_list():
  all_states = lib.template.states(path="/home/shrinidhi/bin/gitHub/dev-ops/tests")
  return simplejson.dumps(all_states.list)

@app.route('/slaves/register',methods=['POST'])
def slaves_register():
  slavedets = simplejson.loads(flask.request.data)
  lib.debug.debug(slavedets)
  try:
    lib.db_sqlite3.execute("insert into slaves (hostid,ip,hostname) values (\"{0}\",\"{1}\",\"{2}\")".format(slavedets['hostid'],slavedets['ip'],slavedets['hostname']))
  except:
    return simplejson.dumps(str(sys.exc_info()))
  return simplejson.dumps("host registered")


@app.route('/slaves/list',methods=['GET'])
def slaves_list():
  try:
    data = lib.db_sqlite3.execute("select * from slaves where status={0}".format(lib.constants.slaves_status.accepted),dictionary=True)
    if(data):
      if(isinstance(data,int)):
        return simplejson.dumps(0)
      else:
        return simplejson.dumps(data)
    else:
      return simplejson.dumps(0)
  except:
    return simplejson.dumps(str(sys.exc_info()))


@app.route('/masterconf',methods=['GET'])
def master_conf():
  return simplejson.dumps(lib.config.master_conf)


@app.route('/slaves/return/result',methods=['POST'])
def slaves_returner():
  result = simplejson.loads(flask.request.data)
  key = result.keys()[-1]
  logfile = os.path.join(lib.constants.m_result_logs_dir,lib.constants.m_result_logs_prefix + lib.constants.m_result_logs_delimiter + str(flask.request.remote_addr) + lib.constants.m_result_logs_delimiter + key + lib.constants.m_result_logs_delimiter + str(time.time()))
  fd = open(logfile,"w")
  fd.write(simplejson.dumps(result[key],indent=4))
  fd.flush()
  fd.close()
  # lib.debug.info(simplejson.dumps(result,indent=4))
  return("ack")



if __name__ == "__main__":
  app.run(host="0.0.0.0",port=lib.config.master_conf['master_rest_port'])

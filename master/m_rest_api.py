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
import multiprocessing


app = flask.Flask(__name__)

@app.route('/states/<hostid>/<state>/<isfile>',methods=['POST'])
def states(hostid,state,isfile):
  slaveconst = simplejson.loads(flask.request.data)
  masterconst = lib.master_utils.masterconst().masterconst()
  all_states = lib.template.states()
  # lib.debug.debug(hostid)
  # lib.debug.debug(state)
  # lib.debug.debug(isfile)
  # lib.debug.debug(slaveconst)
  try:
    ret_state_details = all_states.render(unicode(state), slaveconst=slaveconst,masterconst=masterconst)
  except:
    lib.debug.debug(sys.exc_info())
    return(str(sys.exc_info()))
  # lib.debug.debug(ret_state_details)
  return simplejson.dumps(ret_state_details)

@app.route('/filesync',methods=['POST'])
def filesync():
  slaveconst = simplejson.loads(flask.request.data)
  masterconst = lib.master_utils.masterconst().masterconst()
  all_states = lib.template.states()
  state = slaveconst['file.sync']
  try:
    ret_state_details = all_states.render(unicode(state), slaveconst=slaveconst, masterconst=masterconst, is_file=True)
  except:
    lib.debug.debug(sys.exc_info())
    return(str(sys.exc_info()))
  return (ret_state_details)


@app.route('/getmyip',methods=['GET'])
def getmyip():
  return (flask.request.remote_addr)




@app.route('/high/<hostid>',methods=['POST'])
def high(hostid):
  slaveconst = simplejson.loads(flask.request.data)
  masterconst = lib.master_utils.masterconst().masterconst()
  all_states = lib.template.states()
  lib.debug.debug(slaveconst)
  high_state_obj = all_states.render("high", slaveconst=slaveconst, masterconst=masterconst)

  # valid_states_list = []
  valid_states_list = lib.master_utils.render_high(high_state_obj,slaveconst=slaveconst, masterconst=masterconst)

  state_contents = []
  for x in valid_states_list:
    state_x_content = all_states.render(x,slaveconst=slaveconst,masterconst=masterconst)
    lib.debug.debug(str(x) +" : "+ str(state_x_content))
    if(state_x_content):
      state_contents.extend(state_x_content)

  lib.debug.debug(state_contents)
  return simplejson.dumps(state_contents)


@app.route('/states/list',methods=['GET'])
def states_list():
  all_states = lib.template.states()
  return simplejson.dumps(all_states.list)

@app.route('/slaves/register',methods=['POST'])
def slaves_register():
  slavedets = simplejson.loads(flask.request.data)
  lib.debug.debug(slavedets)
  if(lib.config.master_conf['slave_autoregister']):
    try:
      lib.db_sqlite3.execute("insert into slaves (hostid,ip,hostname,status) values (\"{0}\",\"{1}\",\"{2}\",\"{3}\")".format(slavedets['hostid'], slavedets['ip'], slavedets['hostname'], lib.constants.slaves_status.accepted))
    except:
      return simplejson.dumps(str(sys.exc_info()))
  else:
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

@app.route('/event',methods=['POST'])
def event():
  slaveconst = simplejson.loads(flask.request.data)
  lib.debug.debug(slaveconst['event'])
  event_process = multiprocessing.Process(target=lib.master_utils.event_handler,args=(slaveconst,))
  event_process.start()
  # lib.master_utils.event_handler(slaveconst)
  return (simplejson.dumps([slaveconst['event']]))


if __name__ == "__main__":
  app.run(host="0.0.0.0",port=lib.config.master_conf['master_rest_port'])

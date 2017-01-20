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




app = flask.Flask(__name__)

@app.route('/states/<hostid>/<state>',methods=['POST'])
def states(hostid,state):
  slaveconst = simplejson.loads(flask.request.json)
  all_states = lib.template.states(path="/home/shrinidhi/bin/gitHub/dev-ops/tests")
  ret_state_details = all_states.render(unicode(state),slaveconst=slaveconst)
  # lib.debug.debug(hostid)
  # lib.debug.debug(ret_state_details)
  return simplejson.dumps(ret_state_details)

@app.route('/states/list',methods=['GET'])
def states_list():
  all_states = lib.template.states(path="/home/shrinidhi/bin/gitHub/dev-ops/tests")
  return simplejson.dumps(all_states.list)

@app.route('/register',methods=['POST'])
def register_host():
  slavedets = simplejson.loads(flask.request.json)
  lib.debug.debug(slavedets)
  conn = lib.db_sqlite3.db.connect()
  try:
    conn.execute("insert into slaves (hostid,ip,hostname) values (\"{0}\",\"{1}\",\"{2}\")".format(slavedets['hostid'],slavedets['ip'],slavedets['hostname']))
  except:
    return simplejson.dumps(str(sys.exc_info()))
  return simplejson.dumps("host registered")

@app.route('/register',methods=['POST'])
def register_host():
  slavedets = simplejson.loads(flask.request.json)
  lib.debug.debug(slavedets)
  conn = lib.db_sqlite3.db.connect()
  try:
    conn.execute("insert into slaves (hostid,ip,hostname) values (\"{0}\",\"{1}\",\"{2}\")".format(slavedets['hostid'],slavedets['ip'],slavedets['hostname']))
  except:
    return simplejson.dumps(str(sys.exc_info()))
  return simplejson.dumps("host registered")




@app.route('/masterconf',methods=['GET'])
def master_conf():
  return simplejson.dumps(lib.config.master_conf)



if __name__ == "__main__":
  app.run(host="0.0.0.0",port=lib.config.master_port)

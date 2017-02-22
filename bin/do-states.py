#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
import argparse
import uuid
import zmq
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import lib.constants
import lib.config
import lib.transport
import lib.template
import lib.master_utils
import lib.db_sqlite3
import simplejson

parser = argparse.ArgumentParser(description="Command should be run on master")
parser.add_argument("-l","--list",dest="list",action="store_true",help="list all the states that are available")
parser.add_argument("-n","--hosts",dest="hosts",help="destination hosts to run the states on")
parser.add_argument("-s","--state",dest="state",help="state to run on the hosts")
parser.add_argument("-t","--test",dest="test",help="state to test")
args = parser.parse_args()


if(args.list):
  for x in lib.template.states(path="/home/shrinidhi/bin/gitHub/dev-ops/tests/states_test").list:
    print(x)

else:
  if(args.state):
    lib.debug.debug("running state : "+ args.state)
    uid = str(uuid.uuid4())
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("ipc:///tmp/publisher.zmq.sock")
    socket.send_multipart([uid,args.hosts,args.state])
    validhosts = socket.recv_pyobj()
    for x in validhosts:
      print (x +" : "+ validhosts[x])
    socket.close()
    conn = lib.db_sqlite3.db.connect(lib.constants.mds_sqlite3_file)
    lib.db_sqlite3.execute("insert into log (request_id,state_name,topic) values (\"{0}\",\"{1}\",\"{2}\")".format(uid,args.state,args.hosts),
                           db_file=lib.constants.mds_sqlite3_file)
    print(uid)

  elif(args.test):
    lib.debug.debug("testing state : " + args.test)
    test_state = lib.template.states(path="/home/shrinidhi/bin/gitHub/dev-ops/tests/states_test")
    rendered_state = test_state.render(args.test)
    print (simplejson.dumps(rendered_state,indent=4))


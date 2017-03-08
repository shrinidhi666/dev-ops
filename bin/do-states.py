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
import re
import lib.slave_utils

parser = argparse.ArgumentParser(description="Command should be run on master")
parser.add_argument("-l","--list",dest="list",action="store_true",help="list all the states that are available")
parser.add_argument("-n","--hosts",dest="hosts",help="destination hosts to run the states on")
parser.add_argument("-s","--state",dest="state",help="state to run on the hosts")
parser.add_argument("-t","--test",dest="test",help="state to test")
args = parser.parse_args()


if(args.list):
  for x in lib.template.states().list:
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
    socket.close()
    if(validhosts):
      for x in validhosts:
        print (x +" : "+ simplejson.dumps(validhosts[x],indent=4))
    else:
      print("No valid hosts")
    if(not re.match('^ping\.',args.state)):

      hosts_file = os.path.join(lib.constants.m_result_logs_dir,lib.constants.m_result_logs_prefix_hosts + lib.constants.m_result_logs_delimiter + uid)
      hosts_file_fd = open(hosts_file,"w")
      hosts_file_fd.write(simplejson.dumps(validhosts))
      hosts_file_fd.flush()
      hosts_file_fd.close()


      lib.db_sqlite3.execute("insert into log "
                             "(request_id,state_name,topic) values "
                             "(\"{0}\",\"{1}\",\"{2}\")".format(uid,args.state,args.hosts),
                             db_file=lib.constants.m_dostates_sqlite3_file)
      print("request id : "+ str(uid))

  elif(args.test):
    lib.debug.debug("testing state : " + args.test)
    test_state = lib.template.states()
    slaveconst = lib.slave_utils.slaveconst.slaveconst()
    rendered_state = test_state.render(args.test,slaveconst=slaveconst)
    print (simplejson.dumps(rendered_state,indent=4))


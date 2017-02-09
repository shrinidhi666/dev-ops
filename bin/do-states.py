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

parser = argparse.ArgumentParser()
parser.add_argument("-l","--list",dest="list",action="store_true",help="list all the states that are available")
parser.add_argument("-n","--hosts",dest="hosts",help="destination hosts to run the states on")
parser.add_argument("-s","--state",dest="state",help="state to run on the hosts")

# parser.add_argument("-j","--jobs",dest="jobs")
args = parser.parse_args()


# pub = lib.transport.publisher()
# topic = 2
# state = "level1.level2.level3_1"
# pub.publish(2, {'test': 'x'})
# time.sleep(0.5)
# for x in range(0,10):
#   print (x)
#   pub.publish(topic,state)
#   time.sleep(0.5)

# def

if(args.list):
  for x in lib.template.states(path="/home/shrinidhi/bin/gitHub/dev-ops/tests/states_testl").list:
    print(x)

else:

  uid = str(uuid.uuid4())
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect("ipc:///tmp/publisher.zmq.sock")
  socket.send_multipart([uid,args.hosts,args.state])
  validhosts = socket.recv_pyobj()
  for x in validhosts:
    print (x +" : "+ validhosts[x])
  socket.close()

  print(uid)

  #
  # if(args.hosts):
  #   hosts = []
  #   for h in args.hosts.split(","):
  #     hostemp = lib.master_utils.get_slaves_match(h)
  #     if(hostemp):
  #       hosts.extend(hostemp)
  #   # lib.debug.debug(hosts)
  #   if (args.state):
  #     request_id = uuid.uuid4()
  #     pub = lib.transport.publisher()
  #
  #
  #     for x in hosts:
  #       # print(x['hostname'] + " : " + x['ip'] + " : " + lib.constants.slaves_status()[int(x['status'])])
  #       # pub.publish(x['hostname'], args.state,request_id)
  #       time.sleep(1)
  #       pub.publish(x['hostname'], args.state, request_id)
  #       # time.sleep(1)

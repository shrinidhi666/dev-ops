#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.debug
import lib.transport
import lib.master_utils

import uuid
import zmq


def publisher():
  pub = lib.transport.publisher()
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("ipc:///tmp/publisher.zmq.sock")

  while True:
    #  Wait for next request from client
    (request_id, hostfnmatch, state) = socket.recv_multipart()
    hosts = []
    hostsping = {}
    for h in hostfnmatch.split(","):
      hostemp = lib.master_utils.get_slaves_match(h)
      if (hostemp):
        for ht in hostemp:
          hosts.append(ht['hostid'])

    for x in hosts:
      result = pub.publish(x, state, request_id)
      hostsping[x] = result


    #  Send reply back to client
    socket.send_pyobj(hostsping)


if __name__ == '__main__':
  publisher()
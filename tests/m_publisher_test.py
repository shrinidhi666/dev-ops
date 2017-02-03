#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))


import zmq
import lib.debug
import uuid

uid = str(uuid.uuid4())
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("ipc:///tmp/publisher.zmq.sock")
socket.send_multipart([uid,"blue0*","level1.level2.level3_2.test2"])
test = socket.recv_string()
socket.close()
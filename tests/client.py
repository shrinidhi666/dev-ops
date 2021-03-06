#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.transport
import lib.constants
import uuid

if(__name__ == '__main__'):
  client = lib.transport.client()

  client.send(message_type=lib.constants.tasktypes.host_register,message_type_args={lib.constants.msg_keys.tasktype:lib.constants.tasktypes.key_register,
                                 lib.constants.msg_keys.payload : unicode(uuid.uuid4())})
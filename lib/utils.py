#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import socket
import debug

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


if(__name__ == "__main__"):
  debug.info(ip)
  debug.info(hostname)
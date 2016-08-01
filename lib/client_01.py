#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import core

if(__name__ == '__main__'):
  client = core.client()

  client.send(message={'test':'wtf'})
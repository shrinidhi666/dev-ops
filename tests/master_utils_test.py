#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.master_utils
import lib.slave_utils

ms = lib.master_utils.masterconst(path="/home/shrinidhi/bin/gitHub/dev-ops/tests/master_const")
ss = lib.slave_utils.slaveconst().slaveconst()
mc = ms.masterconst(slaveconst=ss)


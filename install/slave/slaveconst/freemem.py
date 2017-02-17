#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import psutil
import simplejson

def update_consts():
  mem = {}
  vm  = psutil.virtual_memory()
  sw = psutil.swap_memory()
  mem['ram'] = {}
  mem['swap'] = {}
  mem['ram']['total'] = vm.total
  mem['ram']['free'] = vm.free
  mem['swap']['total'] = sw.total
  mem['swap']['free'] = sw.free
  mem['test'] = "True"
  mem['cpu_count'] = psutil.cpu_count()
  return(mem)




if __name__ == '__main__':
    det = update_consts()
    print (det)
#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.constants
import lib.db_sqlite3
import argparse
import glob
import simplejson

parser = argparse.ArgumentParser()
parser.add_argument("-l","--list",dest="list",action="store_true",help="list all the logs")
parser.add_argument("-c","--clean",dest="clean",action="store_true",help="clean all the logs")
parser.add_argument("-o","--order",dest="order",help="asc or dsc order")
parser.add_argument("-s","--show",dest="id",help="show the logs for id ...")
parser.add_argument("-t","--tail",dest="tail",action="store_true",help="tail the logs")
# parser.add_argument("-j","--jobs",dest="jobs")
args = parser.parse_args()
logs = glob.glob(os.path.join(lib.constants.m_result_logs_dir,lib.constants.m_result_logs_prefix + lib.constants.m_result_logs_delimiter +"*"))
ulogs = {}
for x in logs:
  ulogs[x.split(lib.constants.m_result_logs_delimiter)[-2]] = x
if(args.list):
  id_details = lib.db_sqlite3.execute("select * from log",
                                      db_file=lib.constants.mds_sqlite3_file,
                                      dictionary=True)
  for x in id_details:
    print(simplejson.dumps(x,indent=4))
else:
  if(args.id):
    id_details = lib.db_sqlite3.execute("select * from log where request_id=\""+ args.id +"\"",
                                        db_file=lib.constants.mds_sqlite3_file,
                                        dictionary=True)
    print(simplejson.dumps(id_details,indent=4))
    files_to_open = glob.glob(os.path.join(lib.constants.m_result_logs_dir,lib.constants.m_result_logs_prefix + lib.constants.m_result_logs_delimiter +"*"+ args.id +"*"))
    for f in files_to_open:
      fd = open(f,"r")
      data = simplejson.loads(fd.read())
      fd.close()
      print(simplejson.dumps(data,indent=4))
      #
      # for n in data: # hostname
      #   print("\n")
      #   print(n + " : ")
      #   if(isinstance(data[n],dict)):
      #     for o in data[n]: # state_name
      #       print("  "+ str(o) +" : ")
      #       if(isinstance(data[n][o],dict)):
      #         for p in data[n][o]: # state_object
      #           print("    " + str(p) + " : ")
      #           if(isinstance(data[n][o][p],dict)):
      #             for q in data[n][o][p]: # state_module
      #               print("      " + str(q) + " : ")
      #               if(isinstance(data[n][o][p][q],dict)):
      #                 for r in data[n][o][p][q]: # state_module_output . should always have the output status at -1 index : 0 -> success else fail
      #                   if(isinstance(data[n][o][p][q][r],list)):
      #                     if (isinstance(data[n][o][p][q][r][0], list)):
      #                       print("        " + str(r) + " : \n" + str(data[n][o][p][q][r][0][0]))
      #                     if(data[n][o][p][q][r][-1] != 0):
      #                       print ("          FAIL")
      #                     else:
      #                       print ("          SUCCESS")






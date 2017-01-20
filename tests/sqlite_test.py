
#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.db_sqlite3
conn = lib.db_sqlite3.db.connect()

rows = conn.execute("select * from slaves")
for x in rows:
  print(x)


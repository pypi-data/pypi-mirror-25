#!/usr/bin/env python
#-*- coding: utf-8 -*- 
#python 2.7
import sys,os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from collections import OrderedDict as Dict
import markdown


#sys.path.append('/home/share/lib/python')
from functions import * 
import func


def run():
  w=func.Widget()
  w.init()
  w.show()

  if __name__ != "__main__":
    w.exec_()

  return w


if __name__ == "__main__":
  app = QApplication(sys.argv)
  w=run()
  w.setWindowTitle("Dialog")
  sys.exit(app.exec_())

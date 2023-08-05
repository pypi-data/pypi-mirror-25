#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import sys,os
from sys import exit
import time,random
import re
import frd.file

class TextFile(frd.file.File):
  def __init__(self,path):
    frd.file.File.__init__(self,path)

    self.filter_patterns=[]

  def add_filter(self,pattern):
    self.filter_patterns.append(pattern)

  def filter(self):
    for pattern in self.filter_patterns:
      self.remove_lines(pattern)

  def handle(self):
    self.filter()

    #for line_no,line in self.get_lines():
    #  self.validate(line)

    #for line_no,line in self.get_lines():
    #  self.convert(line)


#f=FrdFile.File("Table.txt")
#print f
#print f.info()



#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import sys,os
from random import randint
from time import sleep

import re
"""
  先随意创建方法，再整理

  line_current 以第一行开始

"""

class Object:
  def __init__(self):
    pass

"""
class Line:
  def __init__(self,line):
    pass

    self.spliter=","
    self.cols=line.split(self.spliter)

  def get_cols(self):
    return self.cols

  def get_col(self,number):
    return self.cols[number-1]

  def insert_col_before(self,number,col):
    col=str(col)
    self.cols.insert(number-1,col)

  def insert_col_after(self,number,col):
    col=str(col)
    self.cols.insert(number,col)

  def remove_col(self,number):
    del self.cols[number-1]

  def replace_col(self,number):
    pass

  def __str__(self):
    return self.spliter.join(self.cols)
"""


class File:
  def __init__(self,path):
    self.path=path
    self.lines=[]

    f=open(path,"r+")
    self.lines=f.readlines()
    #clear end "\r\n"
    line_no=0;
    for line in self.lines:
      line=line.rstrip("\n").rstrip("\r")
      self.lines[line_no]=line
      line_no+=1

    f.close()

    #
    self.info=Object()
    self.info.lines=len(self.lines)


    self.line_current=1

  def get_line(self,line_no):
    return self.lines[line_no-1]

  #return line no + line
  def get_lines(self):
    lines=[]

    no=0
    for line in self.lines:
      no+=1
      lines.append((no,line))

    return lines

  def replace_line(self,line_no,line):
    self.lines[line_no-1]=line;

  def remove_line(self,line_no):
    del self.lines[line_no-1]
    self.info.lines=len(self.lines)

  #insert a line before current line
  def insert_line_before(self,line_no,line):
    line+="\n"
    self.lines.insert(self.line_no-1,line)
    #self.line_current-=1;

  #insert a line after current line
  def insert_line_after(self,line):
    line+="\n"
    self.lines.insert(self.line_no,line)
    #self.line_current+=1;

  def replace(self,old_str,new_str):
    for line_no,line in self.get_lines():
      new_line=line.replace(old_str,new_str)
      self.replace_line(line_no,new_line)

    return True
  

  def remove_lines(self,pattern):
    p=re.compile(pattern)
    lines=[]
    for line in self.lines:
      if not p.match(line):
        lines.append(line)
      #else:
      #  print line

    self.reset_lines(lines)
    #self.lines=lines
    #self.info.lines=len(self.lines)

    return True

  def reset_lines(self,lines):
    self.lines=lines
    self.info.lines=len(self.lines)
    pass


  def find_line(self,pattern):
    p=re.compile(pattern)
    index=0
    for line in self.lines:
      index+=1
      match=p.search(line)
      if match:
        self.line_current=index
        return self.line_current
        #return True

    return False

  def remove_empty_lines(self):
    pattern="^( *)$"
    self.remove_lines(pattern)


  def __str__(self):
    return "\n".join(self.lines)

  def save(self,path=False):
    if path == False:
      path=self.path

    f=open(path,'w+')
    contents="".join(self.lines)
    f.write(contents)
    f.close()

    return True

  def info(self):
    print self.info
    #line_count
    # 3 time
    #file size
    #permission
    # writeable, readable
    pass


  def get_current_line(self):
    return self.lines[self.line_current-1]

  def to_line(self,line_no):
    self.line.current=line_no

  def empty(self):
    self.lines=[]
    self.line.current=1


"""
#BASIC USAGE

file=File("a.txt")
file.empty()

line="aaaa"
file.insert_line_after(line)
file.insert_line_after("BBBB")
file.insert_line_after(line)
file.find_line("BBBB")

print file.get_current_line()

file.save()
"""


"""
line=Line("money,100,yesterday")

#print line.get_col(2)
line.insert_col_before(3,200)
line.remove_col(2)
print line
"""

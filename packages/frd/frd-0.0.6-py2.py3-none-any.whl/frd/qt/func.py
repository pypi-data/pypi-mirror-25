#!/usr/bin/env python
#-*- coding: utf-8 -*- 
#python 2.7

import sys,os
import pygame
import time,random

from sys import exit
from random import randint 
from time import strftime
from time import sleep

import hashlib,shutil,time
import urllib,urllib2

from selenium import webdriver

import hashlib,shutil,time
import urllib2
import glob
import pycurl
import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


sys.path.append('/home/share/lib/python')
from functions import *

class Hidden(QLineEdit):
  def __init__(self,parent,name,value=""):
    super(Hidden,self).__init__(parent)

    self.name=name
    self.value=""
    self.data={}

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    return self.value

  def setValue(self,value):
    self.value=value

  def setData(self,k,v):
    self.data[k]=v

  def getData(self,k,default=''):
    if k in self.data:
      return self.data[k]
    else:
      return default


class Label(QtGui.QLabel):
  def __init__(self,parent,name="",value=""):
    super(Label,self).__init__(parent)

    self.setName(name)
    self.setValue(value)

    #最大宽度， 自动换行
    self.setMaximumWidth(600)
    self.setWordWrap(True);

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    return unicode(self.text())

  def setValue(self,value):
    return self.setText(value)

class Image(QtGui.QLabel):
  def __init__(self,parent,name,value):
    super(Label,self).__init__(parent)

    self.setName(name)
    self.setValue(value)

    self.setPixmap(QPixmap(value))

    #最大宽度， 自动换行
    self.setMaximumWidth(600)
    self.setWordWrap(True);

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    return "";

  def setValue(self,value):
    return self.setPixmap(QPixmap(value))

class Input(QLineEdit):
  def __init__(self,parent,name,value=""):
    super(Input,self).__init__(parent)

    self.name=name
    self.setText(value)
    self.data={}

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    return unicode(self.text())

  def setValue(self,value):
    return self.setText(value)

  def setData(self,k,v):
    self.data[k]=v

  def getData(self,k,default=''):
    if k in self.data:
      return self.data[k]
    else:
      return default


class Textarea(QTextEdit):
  def __init__(self,parent,name,value=""):
    super(Textarea,self).__init__(parent)

    self.name=name
    self.setText(value)
    self.data={}

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    return unicode(self.toPlainText())
    #print self.toHtml()

  def setValue(self,value):
    return self.setText(value)

  def setData(self,k,v):
    self.data[k]=v

  def getData(self,k,default=''):
    if k in self.data:
      return self.data[k]
    else:
      return default

class Select(QComboBox):
  def __init__(self,parent,name,value="",options={}):
    super(Select,self).__init__(parent)

    self.options={}
    self.name=name
    self.data={}

    self.setOptions(options)
    self.setValue(value)


  def setOptions(self,options):
    self.options=options

    self.keys=self.options.keys()
    self.values=self.options.values()

    self.addItems(self.values)

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    return unicode(self.keys[self.currentIndex()])

  def setValue(self,value):
    if value in self.keys:
      self.setCurrentIndex(self.keys.index(value))

  def setData(self,k,v):
    self.data[k]=v

  def getData(self,k,default=''):
    if k in self.data:
      return self.data[k]
    else:
      return default


class List(QListWidget):
  def __init__(self,parent,name,value="",options={}):
    super(List,self).__init__(parent)

    self.options={}
    self.name=name
    self.data={}

    self.setOptions(options)
    self.setValue(value)


  def setOptions(self,options):
    self.options=options

    self.keys=self.options.keys()
    self.values=self.options.values()

    i=0
    for value in self.values:
      item=QListWidgetItem(value)
      self.addItem(item)

      #first option choosed as default
      if i == 0:
        self.setCurrentItem(item)

      i+=1

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    row= self.currentIndex().row()

    return unicode(self.keys[row])

  def setValue(self,value):
    if value in self.keys:
      self.setCurrentIndex(self.keys.index(value))

      #self.ui.milestones.setCurrentItem(item)

  def setData(self,k,v):
    self.data[k]=v

  def getData(self,k,default=''):
    if k in self.data:
      return self.data[k]
    else:
      return default

class Button(QPushButton):
  def __init__(self,name,value):
    super(Button,self).__init__(value)

    self.data={}
    self.name=name

  def setName(self,name):
    self.name=name

  def getName(self):
    return self.name

  def getValue(self):
    return unicode(self.text())

  def setValue(self,value):
    self.setText(value)

  def setData(self,k,v):
    self.data[k]=v

  def getData(self,k,default=''):
    if k in self.data:
      return self.data[k]
    else:
      return default


#需要设置handler,处理数据
class FormDialog(QWidget):
  def __init__(self):
    super(FormDialog,self).__init__()

    layout=QFormLayout()
    self.layout=layout
    self.setLayout(layout)





    self.fields={}

    #e=Select(self,"fruits","apple",{
    #  'pear':"Pear",
    #  'apple':'Apple',
    #  'banana':'Banana',
    #})
    #layout.addRow("Fruits",e)

    #button_layout=QHBoxLayout()
    #btn1=Button("save","Save")
    #btn2=Button("cancel","Cancel")

    #button_layout.addWidget(btn1)
    #button_layout.addWidget(btn2)
    #layout.addRow("",button_layout)
    #btn1.clicked.connect(self.on_button_clicked)
    #btn2.clicked.connect(self.on_button_clicked)

    ###menuend
    #x,y,w,h of window
    self.setGeometry(500,500,600,400)
    self.setWindowTitle("PyQt")


  def init_from_config(self,config):
    #config=(
    #  ("text",'domain',u"网站",""),
    #  ("text",'username',u"用户名",""),
    #  ("text",'password',u"密码",""),
    #  ("textarea",'desc', u"备注",""),
    #)

    for row in config:
      field_type,name,label,value=row

      if field_type == "text":
        field=Input(self,name,value)
      elif field_type == "textarea":
        field=Textarea(self,name,value)
      elif field_type == "select":
        field=Select(self,name,value,row[4])
        print len(row)
        if len(row) == 5:
          field.setOptions(row[4])

      self.fields[name]=field
      self.layout.addRow(label,field)

    #buttons
    button_layout=QHBoxLayout()
    btn1=Button("save","Save")
    btn2=Button("cancel","Cancel")

    button_layout.addWidget(btn1)
    button_layout.addWidget(btn2)

    self.layout.addRow("",button_layout)

    btn1.clicked.connect(self.on_button_clicked)
    btn2.clicked.connect(self.on_button_clicked)



  def on_button_clicked(self):
    name=self.sender().getName()

    callback=getattr(self,"on_"+name,None) 
    if not callback:
      raise Exception("method not exists"+" on_"+name)

    callback()

  def on_cancel(self):
    self.close()
    pass

  def on_save(self):
    for field in self.fields.values():
      print field.getName(),field.getValue()
    pass


class Form:
  def __init__(self,parent,layout,config={}):
    self.parent=parent

    self.fields={}

    i=0
    for item in config:

      if item[2] == "hidden":
        pass
      else:
        label = QtGui.QLabel(parent)
        label.setObjectName(_fromUtf8("label"))
        label.setText(item[0])
        #layout.setWidget(i, QtGui.QFormLayout.LabelRole, label)

      if item[2] == "hidden":
        field = Hidden(None,item[1],item[3])
      elif item[2] == "input":
        field = Input(parent,item[1],item[3])
      elif item[2] == "text":
        field = Textarea(parent,item[1],item[3])
      elif item[2] == "select":
        field = Select(parent,item[1],item[3])
        if len(item) == 5:
          field.setOptions(item[4])
      elif item[2] == "label":
        field = Label(parent,item[1],item[3])
      elif item[2] == "image":
        #field = Label(parent,item[1],item[3])
        path=item[3]
        field=Label(parent,item[1],"")
        field.setPixmap(QPixmap(path))


      else:
        print "unknown item type",item[3]

      
      field.adjustSize()
      qsize= field.size()

      #print qsize.width()
      #field.setFixedHeight(qsize.height())



      self.fields[item[1]]=field

      #field.name=item[1]
      if item[2] == "hidden":
        pass
      else:
        layout.addRow(label, field)
        #layout.setWidget(i, QtGui.QFormLayout.FieldRole, field)
        #self.parent.adjustSize()
        #print 'SIZE',self.parent.size()

      i+=1

  def get_params(self):
    params={}

    for name,field in self.fields.items():
      params[name]=field.getValue()


    return params

  def set_params(self,params):
    for name,field in self.fields.items():
      if name in params:
        field.setValue(params[name])

        #print field.size()
        #field.adjustSize()
        #qsize= field.size()

        #print qsize.height()
        #field.setFixedHeight(qsize.height())

  def set_param(self,k,v):
    self.fields[k].setValue(v)



class SearchBar:
  def __init__(self,parent,layout,config={}):
    self.fields={}



    i=0
    for item in config:
      if item[2] == "input":
        field = Input(parent,item[1],item[3])
      elif item[2] == "text":
        field = Textarea(parent,item[1],item[3])

      elif item[2] == "textarea":
        field = Textarea(parent,item[1],item[3])

      elif item[2] == "select":
        field = Select(parent,item[1],item[3])
        if len(item) == 5:
          field.setOptions(item[4])

      else:
        print "unknown item type",item[3]


      self.fields[item[1]]=field

      #field.name=item[1]
      layout.addWidget(field)

      i+=1

  def get_params(self):
    params={}

    for name,field in self.fields.items():
      params[name]=(field.getValue(),field.getData("equal"))


    return params

  def set_params(self,params):
    for name,field in self.fields.items():
      if name in params:
        field.setValue(params[name])


class BaseWidget(QDialog):
  def updatePagination(self,curpage,page_count,item_total):
    curpage=int(curpage)
    page_count=int(page_count)
    item_total=int(item_total)


    page_total=int(math.ceil(item_total/float(page_count)))

    string="  "+"<b>"+unicode(curpage)+"</b>/"+unicode(page_total)
    self.ui.pagination_label.setText(string)

    string=u"%d 项" %(item_total)
    self.ui.pagination_stat.setText(string)


class Widget(QDialog):
  def __init__(self):
    super(Widget,self).__init__()


  def init(self):
    pass

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

class Widget(QDialog):
  def __init__(self):
    super(Widget,self).__init__()


  def init(self):
    self.resize(1147, 784)
    self.setStyleSheet("font: 12pt \"文泉驿等宽微米黑\";")
    self.widget = QWidget(self)
    self.widget.setGeometry(QRect(30, 240, 1011, 521))
    self.widget.setObjectName("widget")
    self.horizontalLayout_2 = QHBoxLayout(self.widget)
    self.horizontalLayout_2.setMargin(0)
    self.horizontalLayout_2.setObjectName("horizontalLayout_2")
    self.msg_list = QListWidget(self.widget)
    self.msg_list.setObjectName("msg_list")
    self.horizontalLayout_2.addWidget(self.msg_list)
    self.verticalLayout = QVBoxLayout()
    self.verticalLayout.setObjectName("verticalLayout")
    self.btn_prev = QPushButton(self.widget)
    self.btn_prev.setObjectName("btn_prev")
    self.verticalLayout.addWidget(self.btn_prev)
    self.label_curpage = QLabel(self.widget)
    self.label_curpage.setObjectName("label_curpage")
    self.verticalLayout.addWidget(self.label_curpage)
    self.label_pagetotal = QLabel(self.widget)
    self.label_pagetotal.setObjectName("label_pagetotal")
    self.verticalLayout.addWidget(self.label_pagetotal)
    self.btn_next = QPushButton(self.widget)
    self.btn_next.setObjectName("btn_next")
    self.verticalLayout.addWidget(self.btn_next)
    spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    self.verticalLayout.addItem(spacerItem)
    self.horizontalLayout_2.addLayout(self.verticalLayout)
    self.widget1 = QWidget(self)
    self.widget1.setGeometry(QRect(30, 10, 1001, 151))
    self.widget1.setObjectName("widget1")
    self.horizontalLayout_3 = QHBoxLayout(self.widget1)
    self.horizontalLayout_3.setMargin(0)
    self.horizontalLayout_3.setObjectName("horizontalLayout_3")
    self.editor = QTextEdit(self.widget1)
    self.editor.setObjectName("editor")
    self.horizontalLayout_3.addWidget(self.editor)
    self.verticalLayout_2 = QVBoxLayout()
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    self.btn_send = QPushButton(self.widget1)
    self.btn_send.setObjectName("btn_send")
    self.verticalLayout_2.addWidget(self.btn_send)
    spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    self.verticalLayout_2.addItem(spacerItem1)
    self.horizontalLayout_3.addLayout(self.verticalLayout_2)

    self.set_text()
    print 'bind'
    self.bind_events()


  def set_text(self ):
      self.setWindowTitle("Dialog")
      self.btn_prev.setText( "上一页")
      self.label_curpage.setText( "aaa" )
      self.label_pagetotal.setText( "bbb" )
      self.btn_next.setText( "下一页" )
      self.btn_send.setText( "发送" )

  def bind_events(self):
    print 'ccc'
    self.btn_send.clicked.connect(self.on_send)

  def on_send(self):
    print 'bbb'
    print self.editor.toPlainText()



def run():
  w=Widget()
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

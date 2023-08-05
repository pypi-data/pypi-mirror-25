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
from func import *



FORM_ADD_CONFIG=(
  (u"目标","target_id","input","TARGET ID"),
  (u"里程碑","milestone_id","input","MILESTONE ID"),
  (u"标题","title","input","TITLE"),
  (u"描述","desc","text",""),
  #(u"图片","img","image",u"/home/frd/private/picture2/别人照片/s.jpg"),
)



class Add(QDialog):
  def __init__(self,parent=None,config={}):
    super(Add,self).__init__(parent)

    self.parent=parent

    self.config=config
    self.init_ui()


  def init_ui(self):
    self.formLayout = QFormLayout(self)
    self.formLayout.setMargin(30)

    #setContentsMargins
    #self.form=Form(self.formLayoutWidget,self.formLayout,config)
    self.form=Form(self,self.formLayout,self.config)
    last_row=len(self.config)+1

    spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.formLayout.setItem(last_row, QFormLayout.LabelRole, spacerItem)

    self.horizontalLayout = QHBoxLayout()
    self.horizontalLayout.setObjectName(u"horizontalLayout")

    spacer= QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacer)


    self.btn_save = QPushButton(self)
    self.btn_save.setText(u"保存");
    self.horizontalLayout.addWidget(self.btn_save)

    self.btn_cancel = QPushButton(self)
    self.btn_cancel.setText(u"取消");
    self.horizontalLayout.addWidget(self.btn_cancel)

    #self.formLayout.setLayout(last_row, QFormLayout.FieldRole, self.horizontalLayout)
    self.formLayout.addRow(self.horizontalLayout)


    self.btn_save.clicked.connect(self.on_save)
    self.btn_cancel.clicked.connect(self.on_cancel)

    self.setMinimumWidth(500)
    self.setMaximumHeight(800)
    
    self.adjustSize()
    #print self.size()

    self.setWindowTitle(u"添加")


  def on_cancel(self):
    self.close()

  def on_save(self):
    params= self.form.get_params()



class ImageViewer(QDialog):
  def __init__(self,parent=None,url=""):
    super(ImageViewer,self).__init__(parent)

    self.parent=parent


    filename=os.path.basename(url)

    path=u"/home/frd/run/image/"+filename
    urllib.urlretrieve(url,path)

    self.config=(
      (u"","image","image",path),
    )


    self.init_ui()


  def init_ui(self):
    self.formLayout = QFormLayout(self)
    self.formLayout.setMargin(30)

    #setContentsMargins
    #self.form=Form(self.formLayoutWidget,self.formLayout,config)
    self.form=Form(self,self.formLayout,self.config)
    last_row=len(self.config)+1

    spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.formLayout.setItem(last_row, QFormLayout.LabelRole, spacerItem)

    self.horizontalLayout = QHBoxLayout()
    self.horizontalLayout.setObjectName(u"horizontalLayout")

    spacer= QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacer)


    self.btn_save = QPushButton(self)
    self.btn_save.setText(u"保存");
    self.horizontalLayout.addWidget(self.btn_save)

    self.btn_cancel = QPushButton(self)
    self.btn_cancel.setText(u"取消");
    self.horizontalLayout.addWidget(self.btn_cancel)

    #self.formLayout.setLayout(last_row, QFormLayout.FieldRole, self.horizontalLayout)
    self.formLayout.addRow(self.horizontalLayout)


    self.btn_save.clicked.connect(self.on_save)
    self.btn_cancel.clicked.connect(self.on_cancel)

    self.setMinimumWidth(500)
    self.setMaximumHeight(800)
    
    self.adjustSize()
    #print self.size()

    self.setWindowTitle(u"添加")


  def on_cancel(self):
    self.close()

  def on_save(self):
    params= self.form.get_params()

if __name__ == "__main__":
  app = QApplication(sys.argv)

  #view=View(None,FORM_UPDATE_CONFIG)
  #view.show()
  add=Add(None,FORM_ADD_CONFIG)
  add.show()

  sys.exit(app.exec_())

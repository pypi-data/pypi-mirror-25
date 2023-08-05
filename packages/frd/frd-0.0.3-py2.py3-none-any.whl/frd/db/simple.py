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


import hashlib,shutil,time
import urllib2
import glob
import pycurl
import pickle


#PATH="/home/share/run/variables.pkl"
PATH="./variables.pkl"
def variable_init(path=False):

  global PATH

  if path:
    PATH=path

  #init
  if not os.path.exists(PATH):
    output=open(PATH,"wb")
    pickle.dump({},output)
    output.close()

def variable_get(name,default=''):
  #get
  output=open(PATH,"rb")
  data=pickle.load(output)

  if name in data:
    return data[name]
  else:
    return default

def variable_set(name,value):
  #set
  output=open(PATH,"rb")
  data=pickle.load(output)
  output.close()

  data[name]=value
  output=open(PATH,"wb")
  pickle.dump(data,output)
  output.close()







#variable_init()
#variable_set('name','100')
#print variable_get('name')

"""
import db.simple as simple
simple.variable_init()
simple.variable_set("name",100)
print  simple.variable_get("name")
print  simple.variable_get("name2",'aaa')
"""

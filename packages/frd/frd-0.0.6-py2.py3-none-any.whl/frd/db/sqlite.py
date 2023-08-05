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

sys.path.append('/home/share/lib/python')
from functions import *


import sqlite3


CONNECTION=None
CURSOR=None

def connect(filename):
  global  CONNECTION , CURSOR

  CONNECTION=sqlite3.connect(filename)
  CURSOR=CONNECTION.cursor()

  return True

def close():
  global CONNECTION

  return CONNECTION.close()

def execute(sql,params=()):
  CURSOR.execute(sql,params)
  CURSOR.commit()


def query(sql,params):
  return execute(sql,params)

def fetchone(sql,params):
  execute(sql,params)
  return CURSOR.fetchone()

def fetchmany():
  execute(sql,params)
  return CURSOR.fetchmany()

def fetchall():
  execute(sql,params)
  return CURSOR.fetchall()


"""
#commit
#rollback
"""


if __name__ == "__main__":
  connect("test.sqlite")

  sql="create table user (id int(10) not null auto_increment primary key)";
  execute(sql)
  

  close()

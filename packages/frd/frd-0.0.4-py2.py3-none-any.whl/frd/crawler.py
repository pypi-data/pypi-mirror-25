#!/usr/bin/env python
#-*- coding: utf-8 -*- 
#python 2.7

import sys,os
import time,random
import hashlib,shutil,time
import urllib,urllib2
import glob
import cookielib


from sys import exit
from random import randint 
from time import strftime
from time import sleep
from bs4 import BeautifulSoup

from frd.functions import *
import frd.db as db
#db.connect('mysql',host="127.0.0.1",username="root",password="",dbname="unicorn") 


def download(url,path):
  try:
      cj=cookielib.CookieJar()
      opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      req = urllib2.Request(url)
      req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.')
      r = opener.open(req)
      return r

  except urllib2.HTTPError:
    return False

  return True

  #return r.read()
  #content=r.read().decode('gbk','ignore').encode('utf-8')
  #content=r.read().decode('gbk','ignore')
  #file_put_contents(path,content)
  #if not os.path.exists(path):
  #  download(URL,path)

def get_soup(content):
  soup=BeautifulSoup(content)

  return soup




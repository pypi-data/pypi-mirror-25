#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import sys,os
from sys import exit
from random import randint 
import time,random
import json
import chardet
from PIL import Image
import hashlib
import requests
import termcolor
import subprocess
import shutil
import codecs
import pprint
from collections import OrderedDict


from urllib import urlencode
from urllib import unquote


import functions

#print functions.iamlosing_api("message.send")

params={
  'page':1,
  'page_count':1,
}
print functions.iamlosing_api("message.find",params)

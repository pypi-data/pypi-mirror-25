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

A4_SIZE=(793,1122)

"""
convert text file's encode to another encode(default utf-8)
will overwrite current file

linux command also can do this:
  iconv -f gbk -t utf-8 1.html  -o 2.html
"""
def convert_file_encode(path,dest_path,to_encode="UTF-8"):
  import chardet

  f=open(path,"r+")
  data=f.read()
  result=chardet.detect(data)
  #print result
  encode=result['encoding']
  #encode="gbk"

  try:
    data=data.decode(encode).encode(to_encode)
  except UnicodeDecodeError:
    if encode == "gb2312":
      encode="gbk"
      print "use gbk replace gb2312 and try again"
      data=data.decode(encode).encode(to_encode)

  #print chardet.detect(data)

  f.close()


  f=open(dest_path, "w")
  f.write(data)
  f.close()



def convert_file_line_split(path,line_split="\n"):
  f=open(path,"r")
  lines=f.readlines()
  f.close()
  new_lines=[]
  for line in lines:
    #clear all \r \n at end
    new_line=line.rstrip("\n").rstrip("\r").rstrip("\n")
    new_lines.append(new_line)


  content=line_split.join(new_lines)

  f=open(path,"w+")
  f.write(content)
  f.close()




def json_encode(data):
  try:
    data=json.dumps(data)
  except ValueError:
    return None
  else:
    return data

def json_decode(data):
  try:
    data=json.loads(data)
  except ValueError:
    return None
  else:
    return data



def file_get_contents(path,encode="utf8"):
  f=codecs.open(path, "r", encode)
  data=f.read()

  #if encode != None:
  #  data=data.decode(encode)

  f.close()

  return data;

def file_put_contents(path,content):
  f=codecs.open(path, "w+", "utf-8")

  f.write(content)
  f.close();

def file_readlines(path):
  content=file_get_contents(path)
  lines=content.split("\n")

  return lines

def today():
  return time.strftime("%Y-%m-%d")

def now():
  return time.strftime("%Y-%m-%d %H:%M:%S")

def gettime(format):
  return time.strftime(format)

def image_size(path):
  im = Image.open(path)
  return im.size

def md5file(fname):
  """ 计算文件的MD5值
  """
  def read_chunks(fh):
    fh.seek(0)
    chunk = fh.read(8096)
    while chunk:
      yield chunk
      chunk = fh.read(8096)
    else: #最后要将游标放回文件开头
      fh.seek(0)

  m = hashlib.md5()
  fh=open(fname, "rb") 
  for chunk in read_chunks(fh):
    m.update(chunk)
    #上传的文件缓存 或 已打开的文件流

  return m.hexdigest()

def current_dir(filepath):
  filename=os.path.abspath(filepath)
  if not os.path.isdir(filename):
    CURDIR=os.path.dirname(os.path.abspath(filepath))
  else:
    CURDIR=filename

  return CURDIR

def strtotime(string,time_format="%Y-%m-%d"):
  return int(time.mktime(time.strptime(string,time_format)))


def file_name(filename):
  filename=os.path.basename(filename)
  names=filename.split(".")
  if len(names) == 1:
    return filename
  else:
    names.pop()
    return ".".join(names)


def file_extension(filename):
  names=filename.split(".")
  if len(names) == 1:
    return ""
  else:
    return names.pop()

def term_red_text(text):
  return termcolor.colored(text,'red')

def term_green_text(text):
  return termcolor.colored(text,'green')

def term_white_text(text):
  return termcolor.colored(text,'white')


def term_color_text(text,color):
  return termcolor.colored(text,color)

def get_folder_filenames(folder):
  filepaths=[]

  for base, dirs, files in os.walk(folder):
    for filename in files:
      filepath=base +"/"+ filename

      filepath=filepath.replace(folder,"").lstrip("/")
      filepaths.append(filepath)


  return filepaths


#returncode,stdout,stderr=execute(cmd)
def execute(cmd):
  p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

  returncode = None
  while returncode is None:
    returncode = p.poll()

  stdout = p.stdout.read()
  stderr = p.stderr.read()

  return (returncode,stdout,stderr)

def http_get(url,params=None):
  r=requests.get(url,params=params)

  if r.status_code != 200:
    #print r.text
    raise BaseException("reponse code not 200: "+unicode(r.status_code))

  try:
    response=r.json()
  except ValueError:
    print r.text
    raise BaseException("reponse text not json format: "+r.text)

  return response

def http_post(url,params=None):
  r=requests.post(url,data=params)

  if r.status_code != 200:
    return {"error":1,"error_msg":"response code invalid "+str(r.status_code)}

  try:
    response=json.loads(r.text)
  except ValueError:
    return {"error":1,"error_msg":"response data invalid \n" +r.text}

  return response

#shutil.copy("readme.txt","a/")


#dest 并不必须是文件名，也可以光指定目录
def copy(src,dest):
  dest_dir=os.path.dirname(dest)

  if not os.path.exists(dest):
    if os.path.isdir(dest):
      os.makedirs(dest)
    else:
      os.makedirs(os.path.dirname(dest))

  shutil.copy(src,dest)

def move(src,dest):
  dest_dir=os.path.dirname(dest)

  if not os.path.exists(dest):
    if os.path.isdir(dest):
      os.makedirs(dest)
    else:
      os.makedirs(os.path.dirname(dest))

  shutil.move(src,dest)

def create_dir(path):
  if path[-1] == "/":
    dir_path=path
  else:
    dir_path=os.path.dirname(path)

  if not os.path.exists(dir_path):
    os.makedirs(dir_path)

def mp3info(filename):
  import mutagen.id3
  import mutagen.id3._util

  info={}

  try:
    fileID3 = mutagen.id3.ID3(filename)

  except mutagen.id3._util.ID3NoHeaderError,e:
    print "get mp3 info failed",e
    return None


  if not fileID3.has_key("TTT2"):
    return None

  if not fileID3.has_key("TPE1"):
    return None

  info['title']= fileID3['TIT2'].text[0]
  info['author']= fileID3['TPE1'].text[0]

  return info


def urlencode_str(string):
  if type(string) == type(u"a"):
    string=string.encode("utf-8")

  return  urlencode({"name":string})[5:]

def http_post_file(url,path,params={}):
  fileobj=open(path,"r")

  filename=os.path.basename(path)
  filename=urlencode_str(filename)
  files={'file': (filename, fileobj)} 
  r = requests.post(url, params,files=files)
  return r

def unicorn_call_api_file(api_name,path,params={}):
  url="http://unicorn.me/api"

  data={
    #"_api":"account:search",
    "_api":api_name,
    "_resource":"public",
  }

  params.update(data)

  print ">>>SEND"
  print "\t\t",url
  print "\t\t",api_name,params
  r= http_post_file(url,path,params)
  print r.status_code,r.text
  try:
    data=r.json()
  except:
    print "invalid response"
    print "\t\t",api_name
    print "\t\t",r.text
    return None

  if data:
    if data['error'] == 0:
      print "success"

      return data
    else:
      print data['error_msg']
      return data
  else:
    print "invalid response",r.text,type(r.text)
    return None

def http_post_json(url,params={}):
  r = requests.post(url, json=params)
  return r

def unicorn_call_api(api_name,params={}):
  url="http://unicorn.me/api"

  data={
    #"_api":"account:search",
    "_api":api_name,
    "_resource":"public",
  }

  params.update(data)

  print ">>>SEND"
  print "\t\t",url
  print "\t\t",api_name,params
  r= http_post_json(url,params)
  #print r.text
  try:
    data=r.json()
  except:
    print "invalid response"
    print "\t\t",api_name
    print "\t\t",r.text
    return None

  if data:
    if data['error'] == 0:
      print "success"

      return data
    else:
      print data['error_msg']
      return False
  else:
    print "invalid response",r.text
    return None

def dump(data):
  pp=pprint.PrettyPrinter(indent=3)
  pp.pprint(data)


#求一个数的任意次根的底数
#   2 ** 3 = 8 , 求8(value) 的3 (root) 次方 
def sqrt2(value,root):
  return  value ** (1. / root)  

def avg(values):
  return round(sum(prices) / float(len(prices)),2)

def middle(values):
  import math

  values=list(values)
  values.sort()
  posi=math.ceil(len(values)/float(2))
  posi=int(posi)
  return values[posi]


def freque(values):
  freques={}

  frequest_count=0
  frequest_values=0

  for value in values:
    if value in freques:
      freques[value]+=1
    else:
      freques[value]=1

  for k,v in  freques.items():
    if v > frequest_count:
      frequest_count=v
      frequest_values=[k,]

    elif v == frequest_count:
      frequest_values.append(k)

  return frequest_values


def iamlosing_api(api_name,params={}):
  #url="https://iamlosing.me/api"
  url="https://iamlosing.me/api"

  #cafile = 'cacert.pem' # http://curl.haxx.se/ca/cacert.pem
  #r = requests.get(url, verify=cafile)

  data={
    #"_api":"account:search",
    "_name":api_name,
  }

  params.update(data)

  #print ">>>SEND"
  #print "\t\t",url
  #print "\t\t",api_name,params
  r= http_post_json(url,params)
  #print r.text
  try:
    data=r.json()
    if data['error'] == 0:
      #print "success"

      return data
    else:
      print "ERROR:",data['error_msg']
      return False

  except:
    #print "invalid response"
    #print "\t\t",api_name
    #print "\t\t",r.text
    print "FAILED:",r.text
    return None

# text必须是16倍数
#msg=encrypt(msg)
def encrypt(text):
  from Crypto.Cipher import AES
  #key 必须是16倍数
  obj = AES.new('KEY_HELLO_WORLD_', AES.MODE_CBC, 'This is an IV456')

  append_text=16 - len(text) % 16 

  text+=append_text * " "

  return obj.encrypt(text)



#msg=encrypt(text)
#text=decrypt(msg)
def decrypt(encrypted_text):
  from Crypto.Cipher import AES
  #key 必须是16倍数
  obj = AES.new('KEY_HELLO_WORLD_', AES.MODE_CBC, 'This is an IV456')

  msg= obj.decrypt(encrypted_text)
  return msg.strip()

"""
    if success: returncode =0  仅仅检查这个即可，有时候errorcode =0,但是stderr也有数据
"""
def execute(cmd):
   p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
   stdout,stderr=p.communicate()
   p.wait()
   
   return (p.returncode,stdout,stderr)


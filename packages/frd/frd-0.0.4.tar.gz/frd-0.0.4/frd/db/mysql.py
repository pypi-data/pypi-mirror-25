#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
 db module, support sqlite3 and mysql
"""

import os,sys
import re

import MySQLdb
import MySQLdb.converters
import MySQLdb.cursors

CONNECTION=None
CURSOR=None


def check_connnect():
  if not CURSOR  or not CONNECTION:
    raise BaseException("db not connected")


def connect(username,password,dbname,params={}):
  global CONNECTION,CURSOR

  try:
    conv=MySQLdb.converters.conversions.copy()

    #数字定义在 MysqlDb.constants/FILE_TYPE.py
    conv[246]=float    # convert decimals to floats
    conv[10]=str       # convert dates to strings
    conv[12]=str       # convert datetime to strings


    #CONNECTION=MySQLdb.connect(host=host,user=username,passwd=str(password),db=dbname,port=port,charset="utf8",cursorclass=MySQLdb.cursors.DictCursor,conv=conv)
    #CONNECTION=MySQLdb.connect(user=username,passwd=str(password),db=dbname,charset="utf8",cursorclass=MySQLdb.cursors.DictCursor,conv=conv)

    params['user']=username
    params['passwd']=unicode(password)
    params['db']=dbname

    params['conv']=conv
    params['charset']="utf8"
    params['cursorclass']=MySQLdb.cursors.DictCursor

    CONNECTION=MySQLdb.connect(**params)


    CURSOR=CONNECTION.cursor()

    CURSOR.execute('set names utf8')
    CONNECTION.commit()

    sql="set character_set_database =  utf8"
    CURSOR.execute(sql)
    CONNECTION.commit()

    sql="set character_set_server =  utf8"
    CURSOR.execute(sql)
    CONNECTION.commit()



  except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return False

  else:
    return True



def disconnect():
  CURSOR.close()
  CONNECTION.close()

  return True



def fetchAll(sql,params=None):
  check_connnect()

  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()
  except BaseException as e:
    print sql
    print "\t", e

  else:
    result=CURSOR.fetchall()
    return result

def fetchOne(sql,params=None):
  check_connnect()

  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()

  except BaseException as e:
    print sql
    print "\t", e


  else:
    result=CURSOR.fetchone()
    if result :
      for k,v in result.items():
        return v
    else:
      return False

def fetchRow(sql,params=None):
  check_connnect()
  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()
  except BaseException as e:
    print sql
    print "\t", e

  else:
    result=CURSOR.fetchone()
    if result :
      return result
    else:
      return False


def execute(sql,params=None):
  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()

    #MySQLdb.paramstyle="qmark"
    #print MySQLdb.paramstyle

  except BaseException as e:
    print sql
    print params
    print "\tError:\t", e
    return False

  else:
    CONNECTION.commit()

  return True

def last_insert_id():
  return CURSOR.lastrowid

##
def build_where(where):
  if len(where) == 0:
    return ''

  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  return where_condition

def build_set(data):
  if len(data) == 0:
    return ''

  set_condition=''

  for k,v in data.items():
    set_condition+=" `%s`='%s' and" %(k,v)

  set_condition=set_condition.rstrip("and")

  return set_condition

#table functions
def get_all(tablename,where):
  sql_params=[]

  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  sql="select * from %s where %s" %(tablename,where_condition)

  try:
    CURSOR.execute(sql,sql_params)
    CONNECTION.commit()
  except BaseException as e:
    print sql
    print "\t", e

  else:
    result=CURSOR.fetchall()
    return result

def get_row(tablename,where):
  sql_params=[]

  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  sql="select * from %s where %s" %(tablename,where_condition)


  try:
    CURSOR.execute(sql,sql_params)
    CONNECTION.commit()
  except BaseException as e:
    print sql
    print "\t", e

  else:
    result=CURSOR.fetchone()
    if result :
      return result
    else:
      return False

def get_one(tablename,where):
  sql_params=[]

  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  sql="select * from %s where %s" %(tablename,where_condition)

  try:
    CURSOR.execute(sql,sql_params)
    CONNECTION.commit()
  except BaseException as e:
    print sql
    print "\t", e

  else:
    result=CURSOR.fetchone()
    if result :
      for k,v in result.items():
        return v
    else:
      return False


def insert(tablename,data):
  keys='`'+"`,`".join(data.keys())+'`'
  values=data.values()

  sql_params=",".join(["%s",]*len(values))

  sql="insert into %s (%s)  values(%s)" %(tablename,keys,sql_params)

  execute(sql,values)

  return CURSOR.lastrowid

def update(tablename,where,data):
  if len(data) == 0:
    return ''


  #sql="update %s set 
  set_condition=''

  sql_params=[]
  set_conditions=[]
  for k,v in data.items():
    set_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  set_condition=",".join(set_conditions)

  #
  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  
  #
  sql="update %s set %s where %s" %(tablename,set_condition,where_condition)

  #print sql 
  #print sql_params
  return execute(sql,sql_params)

def delete(tablename,where):
  if len(where) == 0:
    return ''


  sql_params=[]

  #
  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  
  #
  sql="delete from  %s where %s" %(tablename,where_condition)

  #print sql 
  #print sql_params
  return execute(sql,sql_params)

def exists(tablename,where):
  if len(where) == 0:
    return ''

  sql_params=[]
  #
  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  
  #
  sql="select * from  %s where %s" %(tablename,where_condition)

  try:
      CURSOR.execute(sql,sql_params)
      CONNECTION.commit()
  except BaseException as e:
    print sql
    print sql_params
    print "\t", e

  else:
    result=CURSOR.fetchone()
    if result :
      return True
    else:
      return False

#复合函数
#insert where
#if where exists: update
#else insert
def insert_where(tablename,where,data):
  if exists(tablename,where):
    return update(tablename,where,data)
  else:
    return insert(tablename,data)


#update where 
#if where exists, update
#else do nothing
def update_where(tablename,where,data):
  if exists(tablename,where):
    update(tablename,where,data)

#delete where
#if where exists : delete
def delete_where(tablename,where):
  if exists(tablename,where):
    delete(tablename,where)
    return True
  else:
    return False



###extra
def get_tables(database):
  tables=[]

  rows=fetchAll("show tables in "+database)
  for row in rows:
    name= row.values()[0]
    tables.append(name)

  return tables


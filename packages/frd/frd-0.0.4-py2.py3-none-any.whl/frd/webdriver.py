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

#bool wait_until_url(URL,timeout=10)
def wait_until_url(browser,target_url,timeout=10):
  wait_seconds=0
  while True:
    if browser.current_url != target_url:
      sleep(0.3)
      wait_seconds+=0.3

      #print wait_seconds , browser.current_url
      if wait_seconds > timeout:
        raise BaseException("wait until url too long time: %s" %(target_url))
        return False
    else:
      return True

def find(browser,selector,raise_exception=True):
  node=browser.find_element_by_css_selector(selector)
  if node :
      return node
  else:
      raise BaseException("can not find element :"+selector)


def find_all(browser,css_selector):
  nodes=browser.find_elements_by_css_selector(css_selector)
  return nodes

def click(browser,css_selector):
  item=browser.find_element_by_css_selector(css_selector)
  item.click()


def click_tourl(browser,css_selector,url):
  click(browser,css_selector)
  wait_until_url(browser,url)


def find_timeout(browser,css_selector,timeout=5):
  wait_seconds=0
  while True:
    item=browser.find_element_by_css_selector(css_selector)
    if not item:
      sleep(0.3)
      wait_seconds+=0.3

      #print wait_seconds , browser.current_url
      if wait_seconds > timeout:
        print("wait until url too long time: %s" %(target_url))
        return False
    else:
      return item

def to_url(browser,url):
  browser.get(url)

  wait_seconds=0
  while True:
    if browser.current_url.find(url) != 0:
      sleep(1)
      wait_seconds+=1

       #print wait_seconds , browser.current_url
      if wait_seconds > timeout:
        raise BaseException("wait until url too long time: %s" %(target_url))
        return False

    else:
      return True


def wait_until(func,timeount=20):
  wait_seconds=0
  while True:
    if func() == False:
      sleep(0.3)
      wait_seconds+=0.3

      #print wait_seconds , browser.current_url
      if wait_seconds > timeout:
        raise BaseException("wait until url too long time: %s" %(target_url))
        return False
    else:
      return True

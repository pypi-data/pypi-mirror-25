#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygame,pygame.gfxdraw
from pygame.locals import *
from sys import exit

from PIL import Image ,ImageDraw
from random import randint 
from time import strftime

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
PINK=(255,192,203) 
#深灰
DARKGRAY=(169,169,169)
#暗灰
DIMGRAY=(105,105,105) 


FONT=None
game=None

def get_font_from_file(font_path=None,size=16):
  if not font_path :
    font_path="/home/unicorn/resource/dev_resource/font/方正精品楷体简体.ttf"

  font=pygame.font.Font(font_path,size)

  return font


def get_font(font_name=None,size=16):
  fontnames=("wenquanyimicrohei","arplumingcn","undotum","arplumingtwmbe","vlgothic")
  #fontnames=("vlgothic","wenquanyimicrohei","arplumingcn","undotum","arplumingtwmbe")
  

  font=None
  if not font_name:
    for fontname in fontnames:
      if pygame.font.match_font(fontname):
        print fontname
        font=pygame.font.SysFont(fontname,size)
        break
  else:
    if pygame.font.match_font(font_name):
      font=pygame.font.SysFont(font_name,size)


  if font == None:
    raise BaseException("no avaiable chinese fonts in current locale")

  return font


def sprite_is_collision(sprite,pos):
  x,y,w,h=sprite.rect
  x1,y1=pos

  if x1 > x and x1 < x+w:
    if y1 > y and y1 < y+h:
      return True

  return False


def render_text(font,text,color=WHITE,bgcolor=BLACK):
  lines=text.strip("\n").strip().split("\n")
  width,height=(0,0)

  surfaces=[]
  for line in lines:
    line=line.strip()
    surface=font.render(line,True,color)
    surfaces.append(surface)

    if surface.get_width() > width:
      width= surface.get_width() 

    height+=surface.get_height()+3


  surface=pygame.Surface((width,height))
  surface.fill(bgcolor)
  y=0
  for s in surfaces:
    surface.blit(s,(0,y))
    y+=s.get_height()+3

  return surface


def surface_blit_center(surface,subsurface):
  w,h=surface.get_size()
  width,height=subsurface.get_size()

  x=(w-width)/2
  y=(h-height)/2

  surface.blit(subsurface,(int(x),int(y)))

def random_color():

  r=randint(0,255)
  g=randint(0,255)
  b=randint(0,255)

  return (r,g,b)

class Template:
  def __init__(self,number,title):
    self.title=title
    self.desc=''
    self.number=u"李歌之图形习作第 %d" %(number)
    #self.date=time.strftime("%Y年%m月%d日")
    self.date=u"%s年%s月%s日"  %(strftime("%Y"),strftime("%m"),strftime("%d"))

    self.surface=pygame.Surface((1440,900))
    self.surface.fill(BLACK)

    self.content_surface=pygame.Surface((1000,800))
    self.content_surface.fill(BLACK)
    pass


  def set_desc(self,desc):
    self.desc=desc


  def get_content_surface(self):
    return self.content_surface

  def render(self):
    self.surface.blit(self.content_surface,(440,0))

    #title
    font=get_font(30)
    surface=render_text(font,self.title)
    self.surface.blit(surface,(10,10))

    #desc + date + number
    font=get_font(18)
    if self.desc:
      surface=render_text(font,self.desc)
      self.surface.blit(surface,(10,50))

    surface=render_text(font,self.date)
    self.surface.blit(surface,(10,870))

    surface=render_text(font,self.number)

    x=1440-surface.get_width() - 10
    self.surface.blit(surface,(x,870))

    return self.surface

def random_point(size):
  w,h=size
  x=randint(0,w)
  y=randint(0,h)

  return (x,y)

def createGIF(path,images,duration=0.1,repeat=True):
  from images2gif import writeGif

  writeGif(path,images,duration,repeat)

def time_to_miliseconds(str):
  pattern="(\d+):(\d+):(\d+)(\.\d+)*"
  pattern=re.compile(pattern)
  result=pattern.match(str)
  if not result:
    raise BaseException("invalid time string")

  hour,minute,seconds,miliseconds=result.groups()
  if not miliseconds: miliseconds=0

  hour=int(hour)
  minute=int(minute)
  seconds=int(seconds)
  miliseconds=float(miliseconds)

  total_miliseconds=(hour*3600+minute*60+seconds+miliseconds)*1000
  total_miliseconds=int(total_miliseconds)

  return total_miliseconds


#get all files in a folder
#usage:   get_files(PATH,"*.php")
def get_files( path ,pattern="*"):
  files=[]

  for file in glob.glob(path+"/*"):
    if os.path.isdir(file):
      for file in get_files(file,pattern):
        files.append(file)
    else:
      if glob.fnmatch.fnmatch(file,pattern):
        files.append(file)
        #print file

  return files

def scale(surface,scale_value):
  w,h=surface.get_size()
  w*=scale_value
  h*=scale_value

  w=int(w)
  h=int(h)

  return pygame.transform.scale(surface, (w,h))

def screen_clear(screen):
  screen.fill(BLACK)

def screen_blit_center(screen,surface):
  surface_blit_center(screen,surface)

def value_get(array,key,default=None):
  if array.has_key(key):
    return array[key]
  else:
    return default

class Game:
  def __init__(self,setting={}):
    pygame.init()

    caption=value_get(setting,'caption',"Test Game")
    pygame.display.set_caption(caption)

    self.Screen=pygame.display.set_mode((1440,900),0,32)
    self.Screen.fill(BLACK)
    self.Clock=pygame.time.Clock()
    self.Ticks=0
    self.Ticks_Passed=0
    self._focus_sprite=None
    self._over_sprite=None

    self.Fonts={}
    self.Fonts['default']=get_font(None,24)
    self.Fonts['default24']=get_font(None,24)
    self.Fonts['default30']=get_font(None,30)

    self.Sprites=[]

    #main funcs
    self.init_func=value_get(setting,'init_func')
    self.update_func=value_get(setting,'update_func')
    self.handle_event_func=value_get(setting,'handle_event_func')

    #

  def init(self):
    if self.init_func:
      self.init_func()

  def clear_screen(self):
    self.Screen.fill(BLACK)

  def add_sprite(self,new_sprite):
    for sprite in self.Sprites:
      if sprite.name == new_sprite.name:
        print "same sprite exists: %s" %(name)
        exit(1)

    new_sprite.game=self
    self.Sprites.append(new_sprite)

  def get_sprite(self,name):
    for sprite in self.Sprites:
      if sprite.name == name:
        return sprite

  def render_sprite(self,name):
    sprite=self.get_sprite(name)
    self.Screen.blit(sprite.image,(sprite.rect.x,sprite.rect.y))


  def render_sprites(self):
    for sprite in self.Sprites:
      self.Screen.blit(sprite.image,(sprite.rect.x,sprite.rect.y))

  def handle_event(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        exit()

      if event.type == KEYUP:
        if  event.key == K_ESCAPE:
          exit()
        else:
          if self._focus_sprite:
            self._focus_sprite.handle_event(event)

      elif event.type == MOUSEBUTTONUP:
        pos=event.pos

        choosed=False
        for sprite in self.Sprites:
          if sprite_is_collision(sprite,pos):
            choosed=sprite
            sprite.on_up()
            break

        if not choosed:
          if self._focus_sprite:
            self._focus_sprite.on_blur()
            self._focus_sprite=None

        elif choosed == self._focus_sprite:
          pass
        else:
          if self._focus_sprite:
            self._focus_sprite.on_blur()

          self._focus_sprite=sprite
          self._focus_sprite.on_focus()

      elif event.type == MOUSEBUTTONDOWN:
        pos=event.pos
        for sprite in self.Sprites:
          if sprite_is_collision(sprite,pos):
            sprite.on_down()

      """
      elif event.type == MOUSEMOTION:
        pos=event.pos

        if self._over_sprite:
          if not sprite_is_collision(self._over_sprite,pos):
            self._over_sprite.on_out()
            self._over_sprite=None

        for sprite in self.Sprites:
          if sprite_is_collision(sprite,pos):
            self._over_sprite=sprite
            self._over_sprite.on_over()
      """

  def run(self):
    while True:
      self.handle_event()
      #if self.handle_event_func:
      #  self.handle_event_func(self)

      self.Clock.tick(30) #帧数
      self.Ticks=pygame.time.get_ticks()

      time_passed=self.Ticks-self.Ticks_Passed
      for sprite in self.Sprites:
        sprite.time_tick+=time_passed
        sprite.update()

        if sprite.Render == False:
          self.Screen.blit(sprite.image,(sprite.rect.x,sprite.rect.y))

      self.Ticks_Passed=self.Ticks



      if self.update_func:
        self.update_func(self)

      pygame.display.update()


class Sprite(pygame.sprite.Sprite):
  def __init__(self, name,surface):
    pygame.sprite.Sprite.__init__(self)

    #Flase 相当于需要渲染，True 则是无改变，且已经渲染过了
    self.Render=False 
    self.Hide=False

    self.name=name
    self.time_tick=0

    if surface:
      self.fg_image = surface
      self.bg_image = pygame.Surface(self.fg_image.get_size());
      self.bg_image.fill(BLACK)

      self.rect = self.fg_image.get_rect()

    else:
      self.rect = pygame.Rect(0,0,0,0)
      self.fg_image = None
      self.bg_image = None

    self.image=self.fg_image

  def set_image(self,image):
    self.fg_image=image

    self.bg_image = pygame.Surface(self.fg_image.get_size());
    self.bg_image.fill(BLACK)

    self.image=self.fg_image

    self.rect.w,self.rect.h=image.get_size()

  def move(self,pos):
    self.rect=self.rect.move(pos)

  def set_pos(self,pos):
    self.rect.x,self.rect.y=pos


  def hide(self):
    self.image=self.bg_image
    self.Hide=True

  def show(self):
    self.image=self.fg_image
    self.Hide=False

  def on_focus(self):
    pass

  def on_blur(self):
    pass


  def on_over(self):
    pass

  def on_out(self):
    pass

  #mouse down
  def on_down(self):
    pass

  def on_up(self):
    pass

  def handle_event(self,evt):
    pass


#global variable
class Button(Sprite):
  def __init__(self,name,text):
    self.bgcolor=WHITE
    self.textcolor=BLACK
    self.bordercolor=WHITE
    self.text=text
    self._border_x_space=10
    self._border_y_space=5

    surface=self.render_image()
    Sprite.__init__(self,name,surface)

  def render_image(self):
    #bgsurface=pygame.Su
    #image=render_text(game.Fonts['default'],self.text,BLACK,WHITE)
    image=render_text(game.Fonts['default'],self.text,self.textcolor,self.bgcolor)
    w,h=image.get_size()

    W=w+self._border_x_space*2
    H=h+self._border_y_space*2

    surface=pygame.Surface((W,H))
    surface.fill(self.bgcolor)

    #border
    points=((1,1),(W-1,1),(W-1,H-1),(1,H-1))
    pygame.draw.lines(surface,self.bordercolor,True,points,1)

    #text
    surface.blit(image,(self._border_x_space,self._border_y_space))

    return surface

  def style_click(self):
    self.textcolor=(255,0,0)
    image=self.render_image()
    self.set_image(image)

  """
  def on_over(self):
    self.textcolor=DARKGRAY
    image=self.render_image()
    self.set_image(image)

  def on_out(self):
    self.textcolor=BLACK
    image=self.render_image()
    self.set_image(image)
  """

  def on_down(self):
    self.textcolor=DARKGRAY
    image=self.render_image()
    self.set_image(image)

  def on_up(self):
    self.textcolor=BLACK
    image=self.render_image()
    self.set_image(image)

  def handle_event(self,event):
    pass




"""
1, focus ,闪烁
2， 输入字符
3， 移动光标
4，取消焦点
5,删除字符
6，更好的光标定位
7，从光标位置处理字符


Next:
  支持 ctrl+a 全选
  support  Shift + char (大写)
  不支持特殊字符，不能显示的那种

  高级：支持中文
"""
class Input(Sprite):
  def __init__(self,name):
    Sprite.__init__(self,name,None)

    self.font=game.Fonts['default']
    self.text=""
    self.cursor=0 
    self.cursor_show=False

    self.focus=False
    self.time_internal=1000
    self.time_show=500 #光标显示


    surface=self.get_surface()
    self.set_image(surface)

  def get_surface(self):
    #surface=render_text(game.Fonts['default24'],self.text,self.color)
    width=10*20
    height=self.font.get_height()+10

    surface=pygame.Surface((width,height));
    surface.fill(WHITE)

    #draw border
    #points=((0,1),(width-1,1),(width-1,height-1),(0,height-1))
    points=((1,1),(width-1,1),(width-1,height-1),(1,height-1))
    pygame.draw.lines(surface,BLUE,True,points,1)

    #text
    if self.text:
      surface_text=render_text(self.font,self.text,BLACK,WHITE)
      surface.blit(surface_text,(5,5))

    #cursor
    if self.cursor_show and self.focus:
      s=render_text(self.font,self.text[:self.cursor],BLACK,WHITE)
      w=s.get_width()
      cursor=pygame.Surface((1,self.font.get_height()))
      cursor.fill(BLACK)
      surface.blit(cursor,(w+5,5))

    return surface

  def set_text(self,text):
    self.text=text
    self.cursor=len(self.text)

    self.set_image(self.get_surface())
    self.Render=False

  def append_text(self,text):
    self.text=self.text[:self.cursor]+text+self.text[self.cursor:]
    self.cursor+=len(text)
    self.set_image(self.get_surface())
    self.Render=False

  def delete_char(self):
    self.text=self.text[:self.cursor-1]+self.text[self.cursor:]
    self.cursor-=1
    self.set_image(self.get_surface())
    self.Render=False

  def move_cursor(self,offset_pos):
    self.cursor+=offset_pos
    if self.cursor < 0 : self.cursor =0
    elif self.cursor > len(self.text) : self.cursor = len(self.text)

    self.set_image(self.get_surface())
    self.Render=False

  def on_focus(self):
    self.focus=True

  def on_blur(self):
    self.focus=False
    self.cursor_show=False

    surface=self.get_surface()
    self.set_image(surface);

    self.Render=False

  def handle_event(self,event):
    print event

    if event.type == KEYUP:
      if event.key == K_RETURN:
        pass

      elif event.key == K_LEFT:
        self.move_cursor(-1)
      elif event.key == K_RIGHT:
        self.move_cursor(1)
      elif event.key == K_BACKSPACE:
        self.delete_char()
      else:
        if event.key > 0 and event.key < 256:
          ch=chr(event.key)

          self.append_text(ch);


  def update(self):

    if self.focus:
      if self.time_tick > self.time_internal:
        self.time_tick %=self.time_internal


      if self.time_tick < self.time_show:
        self.cursor_show = True

        surface=self.get_surface()
        self.set_image(surface);
        self.Render=False

      else:
        self.cursor_show = False
        surface=self.get_surface()
        self.set_image(surface);
        self.Render=False

    
class Label(Sprite):
  def __init__(self,name,text):
    Sprite.__init__(self,name,None)

    self.text=text
    self.color=WHITE

    surface=self.get_surface()
    self.set_image(surface)

  def get_surface(self):
    surface=render_text(game.Fonts['default24'],self.text,self.color)
    return surface

  def set_color(self,color):
    self.color=color
    self.set_image(self.get_surface())
    self.Render=False



class Image(Sprite):
  def __init__(self,name,path):
    surface=pygame.image.load(path).convert_alpha()
    Sprite.__init__(self,name,surface)



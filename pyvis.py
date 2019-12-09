import numpy as np
from time import sleep,time
import pygame
import kernel
from vec2 import vec2
screen = None
font = None
width = 256
height = 256

pr_stroke = (255,255,255)
pr_strokeWeight = 1
pr_fill = (255,255,255)
pr_noFill = False

def pyvis_init(): 
    """Init function for pyvis (run this at the beginning of your program)"""
    global screen
    pygame.init()
    screen = pygame.display.set_mode((256,256))
    font = pygame.font.SysFont("arial",18)
def size(x,y): 
    """
    Changes the size of the window
    """
    global screen, width, height ; screen = pygame.display.set_mode((x,y)) ; width = x ; height = y
def frameRate(v): 
    """
    Changes the framerate.
    """
    kernel.pr_framerate = v

def stroke(r,g=-1,b=-1): 
    """
    Changes the stroke color to a grayscale value if 1 argument 
    is given or a rgb color value if 3 arguments are given.
    """
    global pr_stroke ; pr_stroke = (r,r,r) if g == -1 else (r,g,b)
def noStroke():
    global pr_strokeWeight ; pr_strokeWeight = 0
def strokeWeight(w): 
    """
    Changes the width of the stroke (0 indicates no stroke)
    """
    global pr_strokeWeight ; pr_strokeWeight = w
def fill(r,g=-1,b=-1): 
    """
    Changes the fill color to a grayscale value if 1 argument 
    is given or a rgb color value if 3 arguments are given.
    """
    global pr_fill, pr_noFill
    if(pr_noFill): pr_noFill = False
    pr_fill = (r,r,r) if g == -1 else (r,g,b)
def noFill(): 
    """
    Disables the fill
    """
    global pr_noFill ; pr_noFill = True
   
def background(r,g=-1,b=-1): 
    """
    Fills the screen with the given color (grayscale or rgb).
    """
    screen.fill((r,r,r) if g == -1 else (r,g,b))
def line(x1:int,y1:int,x2:int,y2:int,aa=True): 
    if(pr_strokeWeight == 0): return
    if(aa): pygame.draw.aaline(screen,pr_stroke,(x1,y1),(x2,y2),pr_strokeWeight) 
    else: pygame.draw.line(screen,pr_stroke,(x1,y1),(x2,y2),pr_strokeWeight)
def rect(x:int,y:int,w:int,h:int):
    if not pr_noFill: pygame.draw.rect(screen,pr_fill,pygame.Rect(x,y,w,h))
    if pr_strokeWeight > 0: pygame.draw.rect(screen,pr_stroke,pygame.Rect(x,y,w,h),pr_strokeWeight)
def polygon(points):
    if not pr_noFill: pygame.draw.polygon(screen,pr_fill,points)
    if pr_strokeWeight > 0: pygame.draw.polygon(screen,pr_stroke,points,pr_strokeWeight)
def ellipse(x:int,y:int,w:int,h:int):
    if not pr_noFill: pygame.draw.ellipse(screen,pr_fill,pygame.Rect(x,y,w,h))
    if pr_strokeWeight > 0: pygame.draw.ellipse(screen,pr_stroke,pygame.Rect(x,y,w,h),pr_strokeWeight)
def circle(x:int,y:int,r:int):
    if not pr_noFill: pygame.draw.circle(screen,pr_fill,(x,y),r)
    if pr_strokeWeight > 0: pygame.draw.circle(screen,pr_stroke,(x,y),r,pr_strokeWeight)
def label(x:int,y:int,text:str,aa=True):
    screen.blit(font.render(text,aa,pr_fill),(x,y))
def font(name:str,size:int,bf=False,it=False):
    global font ; font = pygame.font.SysFont(name,size,bf,it)
def caption(t:str):
    pygame.display.set_caption(t)
     
def fullscreen(): # currently doesn't work..
    global width, height
    pygame.display.toggle_fullscreen()
    width = screen.get_width()
    height = screen.get_height()

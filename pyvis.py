import numpy as np
import pygame
from time import sleep,time

import kernel
from vec2 import vec2

width = 256
height = 256

_screen = None

_pr_font = None
_pr_stroke = (255,255,255)
_pr_strokeWeight = 1
_pr_fill = (255,255,255)
_pr_noFill = False

_cached_fonts = {}
def pyvis_init(): 
    """Init function for pyvis (run this at the beginning of your program)"""
    global _screen
    pygame.init()
    _screen = pygame.display.set_mode((256,256))
    _pr_font = pygame.font.SysFont("arial",18)
def size(x,y): 
    """
    Changes the size of the window
    """
    global _screen, width, height ; _screen = pygame.display.set_mode((x,y)) ; width = x ; height = y
def frameRate(v): 
    """
    Changes the framerate.
    """
    kernel._pr_framerate = v

def stroke(r,g=-1,b=-1): 
    """
    Changes the stroke color to a grayscale value if 1 argument 
    is given or a rgb color value if 3 arguments are given.
    """
    global _pr_stroke ; _pr_stroke = (r,r,r) if g == -1 else (r,g,b)
def noStroke():
    """
    Disables the stroke around objects. Note: lines will not draw with stroke disabled.
    """
    global _pr_strokeWeight ; _pr_strokeWeight = 0
def strokeWeight(w): 
    """
    Changes the width of the stroke (0 indicates no stroke)
    """
    global _pr_strokeWeight ; _pr_strokeWeight = w
def fill(r,g=-1,b=-1): 
    """
    Changes the fill color to a grayscale value if 1 argument 
    is given or a rgb color value if 3 arguments are given.
    """
    global _pr_fill, _pr_noFill
    if(_pr_noFill): _pr_noFill = False
    _pr_fill = (r,r,r) if g == -1 else (r,g,b)
def noFill(): 
    """
    Disables the fill.
    """
    global _pr_noFill ; _pr_noFill = True
   
def background(r,g=-1,b=-1): 
    """
    Fills the screen with the given color (grayscale or rgb).
    """
    _screen.fill((r,r,r) if g == -1 else (r,g,b))
def line(x1:int,y1:int,x2:int,y2:int,aa=True):
    """
    Draws a line between two points `(x1, y1)` and `(x2, y2)`.
    
    Keyword Arguments:
    - `aa [bool]` -- Enables or disables anti-aliasing (default: `True`)
    """
    if(_pr_strokeWeight == 0): return
    if(aa): pygame.draw.aaline(_screen,_pr_stroke,(x1,y1),(x2,y2),_pr_strokeWeight) 
    else: pygame.draw.line(_screen,_pr_stroke,(x1,y1),(x2,y2),_pr_strokeWeight)
def rect(x:int,y:int,w:int,h:int):
    """
    Draws a rectangle at point `(x,y)` with a given width (`w`) and height (`h`).
    """
    if not _pr_noFill: pygame.draw.rect(_screen,_pr_fill,pygame.Rect(x,y,w,h))
    if _pr_strokeWeight > 0: pygame.draw.rect(_screen,_pr_stroke,pygame.Rect(x,y,w,h),_pr_strokeWeight)
def polygon(points):
    """Draws a polygon from an array of points.
    
    Arguments:
    - `points [list(tuple(int, int))]` -- list of 2D integer tuples representing the points.
    """
    if not _pr_noFill: pygame.draw.polygon(_screen,_pr_fill,points)
    if _pr_strokeWeight > 0: pygame.draw.polygon(_screen,_pr_stroke,points,_pr_strokeWeight)
def ellipse(x:int,y:int,w:int,h:int):
    """
    Draws an ellipse at point `(x,y)` with a given width (`w`) and height (`h`).
    """
    if not _pr_noFill: pygame.draw.ellipse(_screen,_pr_fill,pygame.Rect(x,y,w,h))
    if _pr_strokeWeight > 0: pygame.draw.ellipse(_screen,_pr_stroke,pygame.Rect(x,y,w,h),_pr_strokeWeight)
def circle(x:int,y:int,r:int):
    """
    Draws a circle at point `(x,y)` with a given radius (`r`).
    """
    if not _pr_noFill: pygame.draw.circle(_screen,_pr_fill,(x,y),r)
    if _pr_strokeWeight > 0: pygame.draw.circle(_screen,_pr_stroke,(x,y),r,_pr_strokeWeight)
def label(x:int,y:int,text:str,aa=True):
    """
    Draws a text label at point `(x,y)` with a given text string (`text`)

    Keyword Arguments:
    - `aa [bool]` -- Enables or disables anti-aliasing (default: `True`)
    """
    _screen.blit(_pr_font.render(text,aa,_pr_fill),(x,y))
def font(name:str,size:int,bf=False,it=False):
    """Sets the font used for labels.
    
    Arguments:
        `name [str]` -- Name of the font
        `size [int]` -- Size of the font in pt
    
    Keyword Arguments:
        `bf [bool]` -- makes the text bold (default: False)
        `it [bool]` -- makes the text slanted (default: False)
    """
    global _pr_font
    font_id = f'{name}-{size}'
    font_id += ('-bf' if bf else '') + ('-it' if it else '')
    if font_id in _cached_fonts:
        _pr_font = _cached_fonts[font_id]
    else:
        kernel.log(f"Requesting font [{font_id}] from system",1)
        _pr_font = pygame.font.SysFont(name,size,bf,it)
        _cached_fonts[font_id] = _pr_font
def caption(t:str):
    """
    Sets the title of the application window.
    """
    pygame.display.set_caption(t)
     
def fullscreen(): # currently doesn't work..
    global width, height
    pygame.display.toggle_fullscreen()
    width = _screen.get_width()
    height = _screen.get_height()

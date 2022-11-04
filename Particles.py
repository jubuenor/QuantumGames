import pygame as p
import numpy as np
from Resources import Res
class Particles():
    def __init__(self,x,y,state,ub):
        self.x=x
        self.y=y
        self.state=state
        self.t=1/3
        self.a=180
        self.R=Res(ub).img()
        self.dxd,self.dxa,self.dys,self.dyw=0,0,0,0
    def draw(self,screen):
        if self.a<=344 and self.state!=0:
            self.a+=15*self.state
        else: 
            self.a=0
        img=p.transform.rotozoom(self.R,self.a,self.t)
        centro=img.get_rect(center=(int(self.x),int(self.y)))
        screen.blit(img,centro)
    def resize(self,screen):
        self.set_coords(self.x*screen.get_width()/720,self.y*screen.get_width()/720)
        self.set_t(1/3*screen.get_width()/720)
    def set_coords(self,x,y):
        self.x=x
        self.y=y
    def set_t(self,t):
        self.t=t
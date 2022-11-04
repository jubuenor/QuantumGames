from Particles import Particles
import pygame as p
import numpy as np
import random as r
class Enemy(Particles):
    def __init__(self, x, y, state, ub):
        super().__init__(x, y, state, ub)
        self.x1,self.y1=self.x,self.y
        self.r=0
        self.m=1
        self.d=1
        self.r=-1.25*self.d
    def move(self,x0,y0,screen):
        if self.x<x0:
            self.r=1.25*self.d
        else:
            self.r=-1.25*self.d
        if self.x<=x0-10 or self.x>=x0+10:
            self.m=np.arctan((self.y1-y0)/(self.x1-x0))
            self.y=self.y1+self.r*np.sin(self.m)
            self.x=self.x1+self.r*np.cos(self.m)
        else:
            if self.y<y0:
                self.y=self.y1+1.25*self.d
            else:
                self.y=self.y-1.25*self.d
        self.set_coords(self.x,self.y)
        self.x1,self.y1=self.x,self.y
        if (self.x>screen.get_width()+360*self.t or self.x<-360*self.t) and (self.y>screen.get_height()+180*self.t or self.y<-180*self.t):
            self.reset(screen)
        self.draw(screen)
    def colitions(self,other,screen,music,Game):
        if (self.x-other.x)**2+(self.y-other.y)**2<(130*self.t)**2:
            self.reset(screen)
            if other.num_of_bullets<9:
                if 0<=r.random()<=0.8:
                    other.num_of_bullets+=1
                    music.channel_Play(2)
                else:
                    other.set_coords(r.randint(90*self.t,screen.get_width()-90*self.t),r.randint(90*self.t,screen.get_width()-90*self.t))
            else:
                return True 
        return False       
    def desapear(self):
        self.d*=-1
    def reset(self,screen):
        self.d=1
        self.rad=r.randint(1,8)
        if self.rad==1:
            self.x,self.y=r.randint(int(-300*self.t),int(-100*self.t)),r.randint(int(screen.get_height()+100*self.t), int(screen.get_height()+300*self.t))
        elif self.rad==2:
            self.x,self.y=r.randint(int(-100*self.t),int(screen.get_width()+100*self.t)),r.randint(int(screen.get_height()+100*self.t), int(screen.get_height()+300*self.t))
        elif self.rad==3:
            self.x,self.y=r.randint(int(screen.get_width()+100*self.t),int(screen.get_width()+300*self.t)),r.randint(int(screen.get_height()+100*self.t), int(screen.get_height()+300*self.t))
        elif self.rad==4:
            self.x,self.y=r.randint(int(screen.get_width()+100*self.t),int(screen.get_width()+300*self.t)),r.randint(0, int(screen.get_height()+100*self.t))
        elif self.rad==5:
            self.x,self.y=r.randint(int(screen.get_width()+100*self.t),int(screen.get_width()+300*self.t)),r.randint(int(-300*self.t), int(-100*self.t))
        elif self.rad==6:
            self.x,self.y=r.randint(int(-100*self.t),int(screen.get_width()+100*self.t)),r.randint(int(-300*self.t), int(-100*self.t))
        elif self.rad==7:
            self.x,self.y=r.randint(int(-300*self.t),int(-100*self.t)),r.randint(int(-300*self.t),int(-100*self.t))
        else:
            self.x,self.y=r.randint(int(-300*self.t),int(-100*self.t)),r.randint(int(-self.t*100), int(screen.get_height()+100*self.t))
        self.set_coords(self.x,self.y)
        self.x1,self.y1=self.x,self.y
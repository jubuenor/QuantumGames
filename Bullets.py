from Particles import Particles
import pygame as p
import numpy as np
import random as r
class Bullets(Particles):
    def __init__(self, x, y, state, ub):
        super().__init__(x, y, state, ub)
        self.r=0
        self.move=True
    def colitions(self,other):
        self.d=(self.x-other.x)**2+(self.y-other.y)**2
        if self.d<=1000*self.t:
            self.desapear()
            return True
        return False
    def colitions_Player(self,other,screen,music):
        self.d=(self.x-other.x)**2+(self.y-other.y)**2
        if self.d<=1000*self.t:
            if other.num_of_bullets>=0:
                self.reset(screen)
                other.num_of_bullets-=1
                music.channel_Play(0)
    def shoot(self,a,screen,x,y):
        if self.move:
            self.r+=25*screen.get_width()/720
            self.x=x+self.r*np.cos(a*np.pi/180-np.pi/2)
            self.y=y-self.r*np.sin(a*np.pi/180-np.pi/2)
            self.set_coords(self.x,self.y) 
            self.draw(screen)
    def health(self,screen,player,music,move=True):
        self.vy,self.vx=((self.choice)%2)*25*screen.get_width()/720,((self.choice+1)%2)*25*screen.get_width()/720
        if self.choice==3 or self.choice==2:
            self.vy*=-1
            self.vx*=-1
        if move:
            if -200<=self.x<=screen.get_width()+200 and -200<=self.y<=screen.get_width()+200:
                self.x+=self.vx
                self.y+=self.vy
                self.set_coords(self.x,self.y)
            else:
                self.reset(screen)
        self.colitions_Player(player,screen,music)
        self.draw(screen)
    def reset(self,screen):
        self.choice=r.randint(0,3)
        if self.choice==0:
            self.x0,self.y0=-200*self.t*r.random(),r.randint(int(100*self.t),int(screen.get_height()-100*self.t))
        elif self.choice==1:
            self.y0,self.x0=-200*self.t*r.random(),r.randint(int(100*self.t),int(screen.get_width()-100*self.t))
        elif self.choice==2:
            self.x0,self.y0=screen.get_width()+200*self.t*r.random(),r.randint(int(100*self.t),int(screen.get_height()-100*self.t))
        elif self.choice==3:
            self.y0,self.x0=screen.get_height()+200*self.t*r.random(),r.randint(int(100*self.t),int(screen.get_width()-100*self.t))
        self.set_coords(self.x0,self.y0)
    def desapear(self):
        self.set_coords(p.display.Info().current_w+100,p.display.Info().current_h+100)
        self.move=False
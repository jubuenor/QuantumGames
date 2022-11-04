from Bullets import Bullets
import pygame as p
import numpy as np
import sys
import random as r
from Resources import Res
from Window import Window
from Player import Player
from Enemies import Enemy
class Game():
    def __init__(self,clock):
        p.init()
        self.clock=clock
        self.a=[0,0,0,0,0,0,0,0,0,0]
        self.x0,self.y0=[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]
        self.W=Window(720,720,caption="Save Fermi")
        self.W.start()
        self.music=Res()
        self.player=Player(self.W.screen.get_width()/2,self.W.screen.get_height()/2,1,"Player1.png")
        self.A=self.create_enemies(10)
        self.B=self.create_Health(6)
        self.charge_sounds("Flashpoint001a.wav","pewpew_14.wav","acid5.wav","time_stop.wav","spaceEngine_000.wav","Error or failed.wav","win sound 1-2.wav","Chill.wav","GAMEOVER1.wav","KB - Game Intro Menu Music.wav")
        self.charge_fonts(("DS-DIGI.TTF",20),("DS-DIGI.TTF",100),("DS-DIGI.TTF",40),("Cooper Black Regular.ttf",22),("Cooper Black Regular.ttf",30))
    def charge_sounds(self,*args):
        for i in range(len(args)):
            self.music.sound(args[i],i)
    def charge_fonts(self,*args):
        for i in range(len(args)):
            self.music.font(args[i][0],args[i][1])
    def create_enemies(self,num):
        A=[]
        for i in range(num):
            rad=self.W.screen.get_width()/2*(1+r.random())
            angle=r.random()*2*np.pi
            A.append(Enemy(rad*np.cos(angle)+self.W.screen.get_width()/2,rad*np.sin(angle)+self.W.screen.get_height()/2,-1,"Enemy.png"))
        return A
    def create_Health(self,num):
        B=[]
        for i in range(num):
            B.append(Bullets(0,0,2,"Shoot.png"))
            B[i].reset(self.W.screen)
        return B
    def events(self,event):
        if event.type==p.QUIT:
            p.quit()
            sys.exit()
        if event.type==p.KEYDOWN:
            self.player.move(event.key,True,self.W.screen)
            if event.key==p.K_e:
                if self.W.k==11:
                    self.player.teleport(self.W.screen,self)
                    self.W.k=0
            if event.key==p.K_SPACE:
                if self.player.num_of_bullets<9:
                    self.x0[self.player.num_of_bullets],self.y0[self.player.num_of_bullets],self.a[self.player.num_of_bullets]=self.player.shoot()
                    self.player.Bullets[self.player.num_of_bullets].r=0
                    self.player.Bullets[self.player.num_of_bullets].move=True
                    self.music.channel_Play(1)
            if event.key==p.K_ESCAPE:
                self.W.pause(self)
        if event.type==p.KEYUP:
            self.player.move(event.key,False,self.W.screen)
    def resize(self):
        self.W.resize(self.W.screen.get_width(),self.W.screen.get_height(),self.W.fullscreen)
        self.player.resize(self.W.screen)
        for i in self.A:
            i.resize(self.W.screen)
    def health(self,move=True):
        for i in self.B:
            i.health(self.W.screen,self.player,self.music,move)
    def run(self):
        self.num=0
        self.reset=False
        self.menu=False
        self.Game_Over=False
        self.W.lore(self)
        self.music.music("Dreams of my luck.wav")
        while True:
            self.W.background()
            for event in p.event.get():
                self.events(event)
            for i in range(self.player.num_of_bullets+1):
                self.player.Bullets[i].shoot(self.a[i],self.W.screen,self.x0[i],self.y0[i])
            for i in self.A:
                i.move(self.player.x,self.player.y,self.W.screen)
                if i.colitions(self.player,self.W.screen,self.music,self):
                    self.Game_Over=True
            for j in self.player.Bullets:
                for i in self.A:
                    if j.colitions(i) and i.d>0:
                        i.desapear()
                        self.num+=1
            if self.Game_Over:
                self.reset,self.menu=self.W.game_over(self)
                self.Game_Over=False
            if self.menu:
                self.music.p_music()
                break
            if self.reset:
                self.reset_all()
                self.reset=False
            if self.num%10==0 and len(self.A)<10+5*self.num/10:
                self.A+=self.create_enemies(5)
            self.health()
            self.player.run(self.W.screen)
            self.W.draw_things(self.num,self.player.num_of_bullets)
            p.display.update()
            p.time.Clock().tick(self.clock)
    def draw(self):
        self.W.background()
        for i in self.A:
            i.draw(self.W.screen)
        for i in self.B:
            i.draw(self.W.screen)
        for i in self.player.Bullets:
            i.draw(self.W.screen)
        self.W.draw_things(self.num,self.player.num_of_bullets,False)
        self.player.draw(self.W.screen)
    def reset_all(self):
        self.num=0
        self.W.reset()
        self.player.reset()
        for i in self.B:
            i.reset(self.W.screen)
        for i in self.player.Bullets:
            i.desapear()
        self.A=self.A[:10]
        for i in self.A:
            i.reset(self.W.screen)
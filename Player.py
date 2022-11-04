from Particles import Particles
import random as r
import pygame as p
from Resources import Res
from Bullets import Bullets
import numpy as np
import sys
class Player(Particles):
    def __init__(self, x, y, state, ub):
        super().__init__(x, y, state, ub)
        self.Bullets=[]
        self.num_of_bullets=-1
        for i in range(10):
            self.Bullets.append(Bullets(self.x,self.y,2,"Shoot.png"))    
    def move(self,event,Down,screen):
        if not Down:
            a=5
        else: 
            a=0
        if event==p.K_w:
            self.dyw=(-5+a)*(screen.get_width()/720+(10-self.num_of_bullets)/4)
        if event==p.K_a:
            self.dxa=(-5+a)*(screen.get_width()/720+(10-self.num_of_bullets)/4)
        if event==p.K_d:
            self.dxd=(5-a)*(screen.get_width()/720+(10-self.num_of_bullets)/4)
        if event==p.K_s:
            self.dys=(5-a)*(screen.get_width()/720+(10-self.num_of_bullets)/4)
    def run(self,screen):
        self.draw(screen)
        if self.x>screen.get_width()-90*self.t:
            self.dxd=0
        elif self.x<90*self.t:
            self.dxa=0
        if self.y>screen.get_width()-90*self.t:
            self.dys=0
        elif self.y<90*self.t:
            self.dyw=0
        self.x+=self.dxd+self.dxa
        self.y+=self.dyw+self.dys
        self.set_coords(self.x,self.y)
    def shoot(self):
        if self.num_of_bullets<9:
            self.num_of_bullets+=1
            return self.x,self.y,self.a
    def charge_Estate(self):
        A=[]
        for i in range(5):
            A.append(Res(str(i)+".png").img())
        return A
    def teleport(self,screen,Game):
        Game.music.p_music()
        Game.music.channel_Play(3)
        self.dxa,self.dxd,self.dys,self.dyw=0,0,0,0
        A=self.charge_Estate()
        count=0
        x,y=[self.x,self.x],[self.y,self.y]
        dxa,dxd,dyw,dys=0,0,0,0
        B=False
        d=0
        while True:
            Game.draw()
            d=1-np.sqrt((self.x-x[1])**2+(self.y-y[1])**2)/250
            if d<0:
                d=0
            for event in p.event.get():
                if event.type==p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type==p.KEYDOWN:
                    if event.key==p.K_w:
                        dyw=-8*self.t
                    elif event.key==p.K_s:
                        dys=8*self.t
                    elif event.key==p.K_a:
                        dxa=-8*self.t
                    elif event.key==p.K_d:
                        dxd=8*self.t
                    elif event.key==p.K_e:
                        B=True
                if event.type==p.KEYUP:
                    if event.key==p.K_w:
                        dyw=0
                    elif event.key==p.K_s:
                        dys=0
                    elif event.key==p.K_a:
                        dxa=0
                    elif event.key==p.K_d:
                        dxd=0
            if B:
                Game.music.channel_stop(3)
                self.animate(x,y,d,screen,Game)
                Game.music.u_music()
                break
            if x[1]>screen.get_width()-90*self.t:
                dxd=0
            elif x[1]<90*self.t:
                dxa=0
            if y[1]>screen.get_width()-90*self.t:
                dys=0
            elif y[1]<90*self.t:
                dyw=0
            x[1]+=dxa+dxd
            y[1]+=dyw+dys
            if count<3.2:
                count+=0.8
            else:
                count=0
            for i in range(2):
                self.draw_things(x[i],y[i],A[int(count)],screen)
            Game.music.drawfont(str(int(d*100))+"%",x[1],y[1]-120*self.t,screen,0)
            p.display.update()
            p.time.Clock().tick(Game.clock)
    def decide(self,x,y,d):
        if d>0:
            if 0<=r.random()<=d:
                self.set_coords(x,y)
                return True
        return False
    def animate(self,x,y,d,screen,Game):
        a=0
        count=0
        B=self.charge_Estate()
        Game.music.channel_Play(4)
        while True:
            for event in p.event.get():
                if event.type==p.QUIT:
                    p.quit()
                    sys.exit()
            if a<30:
                a+=0.5
            else:
                if self.decide(x[1],y[1],d):
                    a=1
                    Game.music.channel_Play(6)
                else:
                    a=0
                    Game.music.channel_Play(5)
                Game.music.channel_stop(4)
                break
            if count<3.2:
                count+=0.8
            else:
                count=0
            Game.draw()
            self.draw_things(x[int(a%2)],y[int(a%2)],Res("Player.png").img(),screen)
            self.draw_things(x[abs(int(a%2)-1)],y[abs(int(a%2)-1)],B[int(count)],screen)
            p.display.update()
            p.time.Clock().tick(Game.clock)
    def draw_things(self,x,y,img,screen):
        img=p.transform.rotozoom(img,0,self.t)
        centro=img.get_rect(center=(int(x),int(y)))
        screen.blit(img,centro)
    def resize(self, screen):
        for i in self.Bullets:
            i.resize(screen)
        return super().resize(screen)
    def reset(self):
        self.num_of_bullets=-1
        self.state=1
        self.t=1/3
        self.a=180
        self.R=Res("Player1.png").img()
        self.dxd,self.dxa,self.dys,self.dyw=0,0,0,0

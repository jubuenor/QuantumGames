import pygame as p
from Resources import Res
import random as r
import sys
import numpy as np
class Window():
    def __init__(self,w,h,icon="",caption=""):
        self.w=w
        self.h=h
        self.icon=icon
        self.caption=caption
        self.fullscreen=False
        self.j=0
        self.cota=10
        self.n=0
        self.k,self.ki=0,0
    def start(self):
        if self.icon!="":
            p.display.set_icon(self.icon)
        self.screen = p.display.set_mode((self.w,self.h))
        p.display.set_caption(self.caption)
        self.create_health_bar()
        self.C=[Cells(self.screen.get_width()*(1-170/720),self.screen.get_height()-50*self.screen.get_width()/720)]
    def resize(self,x,y,fullscreen):
        if not fullscreen:
            self.screen = p.display.set_mode((x,y))
        else:
            monitorsize=(p.display.Info().current_w,p.display.Info().current_h)
            self.screen= p.display.set_mode(monitorsize)
    def set_full_screen(self,fullscreen):
        self.fullscreen=fullscreen
    def create_teleport(self):
        B=[]
        for i in range(11):
            B.append(Res("Teletransporte\\"+str(i)+".png").img())
        B.append([Res("Teletransporte\\110.png").img(),Res("Teletransporte\\111.png").img()])
        return B
    def create_health_bar(self):
        self.A=[]
        self.A.append([Res("Salud\\H0.png").img(),Res("Salud\\H0.png").img(),Res("Salud\\H0.png").img(),Res("Salud\\H0.png").img()])
        for i in range(1,11):
            a="Salud\\"
            self.A.append([])
            for j in range(4):
                self.A[i].append(Res(a+"H"+str(i)+str(j)+".png").img())
    def draw(self,img,x,y,a=0,t=1):
        img=p.transform.rotozoom(img,a,t)
        centro=img.get_rect(center=(int(x),int(y)))
        self.screen.blit(img,centro)
    def teleport_bar(self,move=True):
        self.B=self.create_teleport()
        if move:
            if int(self.k)<11:
                self.k+=0.03
            else:
                self.k=11
        if int(self.k)<=10:
            self.draw(self.B[int(self.k)],self.screen.get_width()-50*self.screen.get_width()/720,self.screen.get_height()-130*self.screen.get_width()/720)
        else:
            if self.ki<1.8:
                self.ki+=0.2
            else:
                self.ki=0
            self.draw(self.B[11][int(self.ki)],self.screen.get_width()-50*self.screen.get_width()/720,self.screen.get_height()-130*self.screen.get_width()/720)
    def health_bar(self,num_of_bullets):
        if self.j<3.6:
            self.j+=0.3
        else:
            self.j=0
        if num_of_bullets>=0:
            self.draw(self.A[abs(num_of_bullets-9)][int(self.j)],self.screen.get_width()-100*self.screen.get_width()/720,self.screen.get_height()-130*self.screen.get_width()/720)
        else:
            self.draw(self.A[10][int(self.j)],self.screen.get_width()-100*self.screen.get_width()/720,self.screen.get_height()-130*self.screen.get_width()/720)
    def cells(self,num):
        if num>=self.cota:
            self.n+=1
            self.C.append(Cells(self.screen.get_width()*(1-(170+self.n*45)/720),self.screen.get_height()-50*self.screen.get_width()/720))
            self.cota*=10
        for i in range(len(self.C)):
            self.C[i].animate(int(str(num)[-i-1]),self.screen)
    def background(self):
        img=Res("Grid1.png").img(False)
        img=p.transform.rotozoom(img,0,self.screen.get_width()/720)
        centro=img.get_rect(center=(int(self.screen.get_width()/2),int(self.screen.get_height()/2)))
        self.screen.blit(img,centro)
    def draw_things(self,num,num_of_bullets,move=True):
        self.cells(num)
        self.health_bar(num_of_bullets)
        self.teleport_bar(move)
    def pause(self,Game):
        Game.music.p_music()
        Game.music.set_volume(0.2,7)
        Game.music.channel_Play(7,-1)
        i=255
        j=255
        k=255
        count=0
        b=False
        while True:
            for event in p.event.get():
                if event.type==p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type==p.KEYDOWN:
                    if event.key==p.K_ESCAPE:
                        b=True
            if b:
                Game.music.u_music()
                Game.music.channel_stop(7)
                break
            if count<10:
                count+=1
            else:
                count=0
                i=r.randint(0,255)
                j=r.randint(0,255)
                k=r.randint(0,255)
            Game.draw()
            Game.music.drawfont("Pausa",Game.W.screen.get_width()/2,Game.W.screen.get_width()/2,Game.W.screen,1,(i,j,k))
            p.display.update()
            p.time.Clock().tick(Game.clock)
    def game_over(self,Game):
        Game.music.p_music()
        Game.music.channel_Play(8)
        i=255
        j=255
        k=255
        count=0
        b=False
        c=False
        Game.player.t=1
        while True:
            self.background()
            for event in p.event.get():
                if event.type==p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type==p.KEYDOWN:
                    if event.key==p.K_RETURN:
                        b=True
                    if event.key==p.K_ESCAPE:
                        c=True
            if b or c:
                Game.music.u_music()
                Game.music.channel_stop(8)
                if b:
                    return True,False
                if c:
                    return False,True
            
            if count<10:
                count+=1
            else:
                count=0
                i=r.randint(0,255)
                j=r.randint(0,255)
                k=r.randint(0,255)
            if Game.player.state>-1:
                Game.player.state-=0.01
            if Game.player.state<=0:
                Game.player.R=Res("Enemy.png").img()
            Game.player.set_coords(Game.W.screen.get_width()/2,Game.W.screen.get_width()/2)
            Game.player.draw(Game.W.screen)
            Game.music.drawfont("Game Over",Game.W.screen.get_width()/2,Game.W.screen.get_width()/2-150,Game.W.screen,1,(i,j,k))    
            Game.music.drawfont("Presiona 'Enter' para reiniciar.",Game.W.screen.get_width()/2,Game.W.screen.get_width()-100,Game.W.screen,2,(i,255,k)) 
            Game.music.drawfont("o presiona 'Escape' para ir al menu.",Game.W.screen.get_width()/2,Game.W.screen.get_width()-50,Game.W.screen,2,(i,255,k)) 
            p.display.update()
            p.time.Clock().tick(Game.clock)
    def lore(self,Game):
        Game.music.channel_Play(9,-1)
        img1=[]
        for i in range(2):
            img1.append([])
            for j in range(17):
                img1[i].append(Res("Lore\\"+str(i)+str(j)+".png").img())
        img1.append(Res("Player.png").img())
        img1.append(Res("Enemy.png").img())
        img2=[Res("Player1.png").img(),Res("Shoot.png").img(),Res("Lore\\Fermi.png").img()]
        img3=[]
        for i in range(5):
            img3.append(Res(str(i)+".png").img())
        Text1=["Espín",
                "El espín es una propiedad física de las partículas que está", "asociada con la rotación de estas, más puntualmente con", "el momento magnético.",
                "Existen partículas de espín entero (1,2,3,4,...), las cuales", "se llaman Bosones.",
                "Y luego estamos nosotros los fermiones partículas con espín", "semi-entero (1/2,3/2,5/2,...).",
                "Los fermiones se diferencian de los bosones por la manera", "en que interactúan entre ellos."
                ]
        Text2=["Principio de exclusión de Fermi",
                "Este principio establece que dos Fermiones no pueden", "compartir el mismo estado cuántico (ni de posición","ni de espín).",
                "Con lo cual estos electrones de spín -1/2 quieren estar", "en mi estado cuántico, nuestro objetivo es no permitirlo.", "Subiendo sus niveles de energía a través de los fotones que", "puedo lanzar al presionar 'Espacio'.",
                "Debemos salvar a Fermi..."
                ]
        Text3=["Como mi estado cuántico no está completamente definido", "mi imagen representa la posición más probable en", "el espacio. Por tanto podemos redefinir está posición", "usando la letra 'E'.",
                "Si los otros electrones nos golpean tienen un 80% de", "probabilidad de bajarnos el nivel de energía en un", "fotón y un 20% de redefinir nuestra actual posición,", "si perdemos todos los fotones es probable que mi espín", "cambie.",
                "Resiste lo más que puedas..."
                ]
        count1=0
        i,j,k=255,255,255
        b,c1=0,0
        sx=200
        Texts=[Text1,Text2,Text3]
        x,y=[360,360],[300,300]
        a=0
        t=np.zeros(len(Texts[0]))
        r0=0
        count=0
        while True: 
            self.screen.fill((0,0,0))           
            self.draw(Res("grid_bg.png").img(),self.screen.get_width()/2,self.screen.get_height()/2)
            for event in p.event.get():
                if event.type==p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type==p.KEYDOWN:
                    if event.key==p.K_RETURN:
                        b+=1
                        a=0
                        c1=1
                        if b<=2:
                            t=np.zeros(len(Texts[b]))
            if b==0:
                if a<=344:
                    a+=15
                else: 
                    a=0
                for i in range(len(t)):
                    if t[i]<len(Text1[i]):
                        t[i]+=1
                Game.music.drawfont(Text1[0][:int(t[0])],20,80,self.screen,4,(255,255,255),False)
                for i in range(1,4):
                    Game.music.drawfont(Text1[i][:int(t[i])],45,120+(i-1)*20,self.screen,3,(1,216,119),False)
                if c1<16.2:
                    c1+=0.8
                else:
                    c1=0
                for i in range(2):
                    self.draw(img1[i][int(c1)],285+i*150,240)
                for i in range(4,8):
                    Game.music.drawfont(Text1[i][:int(t[i])],45,300+(i-4)*20,self.screen,3,(1,216,119),False)
                Game.music.drawfont("Espín=1/2",285,430,self.screen,3,(255,255,255))
                Game.music.drawfont("Espín=-1/2",435,430,self.screen,3,(255,255,255))
                for i in range(2):
                    self.draw(img1[i+2],285+i*150,500,a*(1-2*i),1/2)
                for i in range(2):    
                    Game.music.drawfont(Text1[-1-i][:int(t[-1-i])],45,600-i*20,self.screen,3,(255,255,255),False)
            elif b==1:
                if a<=344:
                    a+=15
                else: 
                    a=0
                for i in range(len(t)):
                    if t[i]<len(Text2[i]):
                        t[i]+=1
                Game.music.drawfont(Text2[0][:int(t[0])],20,80,self.screen,4,(255,255,255),False)
                for i in range(1,4):
                    Game.music.drawfont(Text2[i][:int(t[i])],45,120+(i-1)*20,self.screen,3,(1,216,119),False)
                self.draw(img2[2],360,240,0,1/2)
                for i in range(4,8):
                    Game.music.drawfont(Text2[i][:int(t[i])],45,300+(i-4)*20,self.screen,3,(1,216,119),False)
                if sx<520:
                    sx+=20
                else:
                    sx=200
                self.draw(img2[1],sx,500,2*a,1/2)
                self.draw(img2[0],200,500,90,1/2)
                Game.music.drawfont(Text2[-1][:int(t[-1])],45,600,self.screen,3,(255,255,255),False)
            elif b==2:
                for i in range(len(t)):
                    if t[i]<len(Text3[i]):
                        t[i]+=1
                for i in range(4):
                    Game.music.drawfont(Text3[i][:int(t[i])],45,120+(i-1)*20,self.screen,3,(1,216,119),False)
                if count<3.2:
                    count+=0.8
                else:
                    count=0
                for i in range(2):
                    self.draw(img3[int(count)],x[i],y[i],0,1/3)
                d=1-np.sqrt((x[0]-x[1])**2+(y[0]-y[1])**2)/250
                a+=0.1
                if r0<100 and c1==1:
                    r0+=0.8
                else:
                    c1=-1
                if c1==-1 and r0>0:
                    r0-=0.8
                else:
                    c1=1
                x[1],y[1]=x[0]+r0*np.cos(a),y[0]+r0*np.sin(a)
                Game.music.drawfont(str(int(d*100))+"%",x[1],y[1]-40,self.screen,0)
                for i in range(4,9):
                    Game.music.drawfont(Text3[i][:int(t[i])],45,450+(i-4)*20,self.screen,3,(1,216,119),False)
                Game.music.drawfont(Text3[-1][:int(t[-1])],45,600,self.screen,3,(255,255,255),False)
            elif b==3:
                Game.music.channel_stop(9)
                break
            if count1<10:
                count1+=1
            else:
                count1=0
                i=r.randint(0,255)
                j=r.randint(0,255)
                k=r.randint(0,255)
            Game.music.drawfont("Presiona 'Enter' para continuar.",350,680,self.screen,3,(i,j,k),False)
            p.display.update()
            p.time.Clock().tick(Game.clock)
    def reset(self):
        self.j=0
        self.cota=10
        self.n=0
        self.k,self.ki=0,0
class Cells():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.create_cells()
        self.j=0
    def create_cells(self):
        self.A=[]
        for i in range(61):
            self.A.append(Res("Contador\\"+str(i)+".png").img())
    def draw(self,img,screen):
        img=p.transform.rotozoom(img,0,screen.get_width()/720)
        centro=img.get_rect(center=(int(self.x),int(self.y)))
        screen.blit(img,centro)
    def animate(self,num,screen):
        if self.j<num*6:
            self.j+=0.7
        if num*6>59.3 or num==0:
            self.j=0
        self.draw(self.A[int(self.j)],screen)
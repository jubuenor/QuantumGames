from Game import Game
from PongQu import PongQu
import random as r
import pygame as p
import sys
from Resources import Res
class Main():
    def __init__(self):
        self.screen = p.display.set_mode((1280, 720))
        self.Background=Res("Main\\Background.png").img()
        self.im0=Res("Main\\0.png").img()
        self.im1=Res("Main\\1.png").img()
        self.font=Res()
        self.font.music("menu_chill1.wav")
        self.charge_fonts(("Roblox Font Black.ttf",100),("nasalization-rg.otf",30),("nasalization-rg.otf",15))
        p.display.set_caption("Quantum Games")
    def charge_fonts(self,*args):
        for i in range(len(args)):
            self.font.font(args[i][0],args[i][1])
    def run(self):
        ray=[]
        text=["Los juegos se encuentran en  superposición cuántica, al darclick sobre", "'Quantum Games' podrás jugar uno de los dos con un 50% de probabilidad.", "Suerte."]
        for i in range(11):
            ray.append(Res("Main\\lightning\\"+str(i)+".png").img())
        countr=0
        i=[1280/2-300,1280/2+300]
        count=0
        pos=(0,0)
        change=False
        while True:
            if countr<len(ray)-1.5:
                countr+=0.5
            else:
                countr=0
            if count<1.5:
                count+=0.05
            else:
                count=0
            self.draw(self.Background,1280/2,720/2)
            self.draw(ray[int(countr)],1280/2,720/2-200)
            self.draw(self.im0,i[abs(int(count)-1)],720/2-200)
            self.draw(self.im1,i[int(count)],720/2-200)
            self.font.drawfont("Quantum Games",1280/2,720/2,self.screen,0,(1,216,119))
            self.font.drawfont(text[0],45,550,self.screen,1,(255,255,255),False)
            self.font.drawfont(text[1],45,580,self.screen,1,(255,255,255),False)
            self.font.drawfont(text[2],1280/2,630,self.screen,1,(255,255,255))
            self.font.drawfont("Un juego hecho por: Juan Bueno y Jhon Moreno",880,690,self.screen,2,(255,255,255),False)
            for event in p.event.get():
                if event.type==p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type == p.MOUSEBUTTONUP:
                    pos = p.mouse.get_pos()
            if 220<=pos[0]<=1059 and 317<=pos[1]<=388:
                change=True
                pos=(0,0)
            if change:
                self.font.p_music()
                if r.random()<=0.5:
                    self.G1=PongQu()
                    self.screen = p.display.set_mode((1280, 720))
                    self.G1.run()
                else:
                    self.G0=Game(60)
                    self.G0.run()
                    self.screen = p.display.set_mode((1280, 720))
                change=False
                self.font.music("menu_chill1.wav")
            p.display.update()
            p.time.Clock().tick(60)
    def draw(self,img,x,y,a=0,t=1):
        img=p.transform.rotozoom(img,a,t)
        centro=img.get_rect(center=(int(x),int(y)))
        self.screen.blit(img,centro)
A=Main()
A.run()

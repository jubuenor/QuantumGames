import pygame as p
from pygame import mixer
class Res():
    def __init__(self,a=""):
        self.ubicacion=a
        self.channels=[]
        self.sounds=[]
        self.fonts=[]
        mixer.init()
        mixer.set_num_channels(10)
    def img(self,alpha=True):
        if alpha:
            return p.image.load("Images\\"+self.ubicacion).convert_alpha()
        return p.image.load("Images\\"+self.ubicacion).convert()
    def sound(self,sound,n):
        self.sounds.append(mixer.Sound("Sounds\\"+sound))
        self.channels.append(mixer.Channel(n))
    def channel_Play(self,n,times=0):
        self.channels[n].play(self.sounds[n],times)
    def channel_stop(self,n):
        self.channels[n].stop()
    def set_volume(self,v,n):
        self.channels[n].set_volume(v)
    def music(self,ub):
        mixer.music.load("Sounds\\"+ub)
        mixer.music.play(-1)
    def p_music(self):
        mixer.music.pause()
    def u_music(self):
        mixer.music.unpause()
    def font(self,ub,size):
        self.fonts.append(p.font.Font("Fuentes\\"+ub,size))
    def drawfont(self,txt,x,y,screen,n,color=(0,255,0),center=True):
        tx=self.fonts[n].render(txt,True,color)
        if center:
            screen.blit(tx,tx.get_rect(center=(int(x),int(y)))) 
        else:
            screen.blit(tx,(x,y)) 


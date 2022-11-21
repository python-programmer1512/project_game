import sys
import random
import pygame
import time
import math
FPSCLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((900,900))
class stamina_item(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        X=x#random.randint(40,860)
        Y=y#random.randint(40,860)
        self.img=pygame.image.load("bandage.png").convert_alpha()
        self.img=pygame.transform.scale(self.img,(45,45))#(56,60))
        self.mask=pygame.mask.from_surface(self.img)
        #else:
        self.SURFACE=SURFACE
        self.rect=self.img.get_rect()
        self.X=X
        self.Y=Y
        self.rect.center=(self.X,self.Y)#x=self.X
        #self.rect.centery=self.Y
    def draw(self):
        #self.rect.centerx=self.X
        #self.rect.centery=self.Y
        self.SURFACE.blit(self.img,self.rect)#(self.rect.centerx,self.rect.centerx))
    def keyboard_move(self,x):
        global A,B
        #print("#",self.X,self.Y)
        if x==1:self.Y+=3
        elif x==2:self.X-=3
        elif x==3:self.X+=3
        elif x==4:self.Y-=3
        #if x==1:self.Y+=3;A.Y+=3;zombie_move(0.2,1)
        #elif x==2:self.X-=3;A.X-=3;zombie_move(0.2,2)
        #elif x==3:self.X+=3;A.X+=3;zombie_move(0.2,3)
        #elif x==4:self.Y-=3;A.Y-=3;zombie_move(0.2,4)
        self.rect.center=(self.X,self.Y)
        #print("##",self.X,self.Y)

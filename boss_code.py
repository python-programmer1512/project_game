import sys
import random
import pygame
import time
#import mainprogram as mp
import math
FPSCLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((900,900))
class boss_zombie_life():
    def __init__(self,mlife):
        self.SURFACE=SURFACE
        self.img=pygame.image.load("bar.png")
        self.img1=pygame.image.load("life.png")
        self.imgx=mlife+60
        self.imgy=13
        self.img=pygame.transform.scale(self.img,(self.imgx,self.imgy))
        self.ship_image_pos= self.img.get_rect()
        self.ship_image_pos.center=(450,450)
        self.show=0
        self.time=0
        self.rt=100
        #self.SURFACE.blit(self.img,self.ship_image_pos)
    def bar_draw(self,mlife,life,x,y):
        self.img1=pygame.transform.scale(self.img1,(max(0,self.imgx/mlife*life),self.imgy))
        self.show=1
        #self.SURFACE.blit(self.img,self.ship_image_pos)
        #self.SURFACE.blit(self.img1,(x-self.imgx/2,y-50-self.imgy/2))
    def bar_alone(self,x,y):
        if self.show==1:
            self.time+=1
            if self.time==self.rt:
                self.show=0
                self.time=0
                return
            self.ship_image_pos.center=(x,y-50)
            self.SURFACE.blit(self.img,self.ship_image_pos)
            self.SURFACE.blit(self.img1,(x-self.imgx/2,y-50-self.imgy/2))
class boss_zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img=pygame.image.load("bz1.png").convert_alpha()
        self.img=pygame.transform.scale(self.img,(241*80/235,80))#(56,60))
        self.X=random.randint(-100,1000)#(-100,1000)
        if self.X<0 or self.X>900:
            self.Y=random.randint(-100,1000)#(-100,1000)
        else:
            qtre=random.randint(1,2)
            if qtre==1:self.Y=random.randint(-100,0)
            else:self.Y=random.randint(900,1000)
        self.mask=pygame.mask.from_surface(self.img)
        self.rect=self.img.get_rect()
        self.rect.center=(self.X,self.Y)
        self.img_number=0
        self.angle=0
        self.SURFACE=SURFACE
        self.life=60#20
        self.max_life=60#20
        self.bar=boss_zombie_life(self.max_life)
        self.img_size_idx=0
        self.lisi=0
        self.ds=0
        self.ig_idx_move=1
        self.img_size=[[241*80/235,80],[270*80/235,80],[287*80/235,80],[295*80/235,80],[128,377/2.9375]]
        #self.img_size=[[69,60],[231*60/182,60.66666666666667],[240*60/182,60.66666666666667],[244*60/182,60.66666666666667],[253*60/182,60.66666666666667]]
    def watch_player(self):
        #global A
        self.angle=math.pi-math.atan2(self.X-450,self.Y-450)
        FG=-(int(math.degrees(self.angle)))-90#+90
        rotation_ship_image= pygame.transform.rotate(self.img,FG)
        self.rect= rotation_ship_image.get_rect()
        px=0
        py=0
        #A.
        #self.xd=math.sin(math.radians(FG+90))
        #self.yd=math.cos(math.radians(FG+90))
        if math.sqrt(abs(450-self.X)**2+abs(450-self.Y)**2)>100:
            self.X+=math.sin(math.radians(FG+90))*1
            self.Y+=math.cos(math.radians(FG+90))*1
            self.ig_idx_move=1
            #self.lisi=self.img_size_idx
            self.img_size_idx=0
            if self.lisi==0:
                self.img=pygame.image.load("bz"+str(self.img_size_idx//5+1)+".png").convert_alpha()
                self.img=pygame.transform.scale(self.img,(self.img_size[self.img_size_idx//5][0],self.img_size[self.img_size_idx//5][1]))#(56,60))
                self.lisi=1
        else:
            self.lisi=0
            R=self.img_size[self.img_size_idx//5][0]-self.img_size[0][0]
            px=math.sin(math.radians(FG+90))*R/2#*0.5#*0#.001#*1.5#*2
            py=math.cos(math.radians(FG+90))*R/2
            if self.ig_idx_move==1:
                #*0.5#*0#.001#*1.5
                #self.lisi=self.img_size_idx
                self.img_size_idx+=1
                if self.img_size_idx//5>=5:self.img_size_idx=5*5;self.ig_idx_move=-1;self.ds+=10
            if self.ig_idx_move==-1:
                #self.lisi=self.img_size_idx
                self.img_size_idx-=1
                if self.img_size_idx//5<0:self.img_size_idx=0;self.ig_idx_move=1
            #if self.img_size_idx//100<0 or self.img_size_idx//5>=5:
               #print(self.img_size_idx%100)
            #print(A.life)
            self.img=pygame.image.load("bz"+str(self.img_size_idx//5+1)+".png").convert_alpha()
            if self.img_size_idx//3<0 or self.img_size_idx//5>=5:print(self.img_size_idx)
            self.img=pygame.transform.scale(self.img,(self.img_size[self.img_size_idx//5][0],self.img_size[self.img_size_idx//5][1]))#(56,60))
        #self.X+=px
        #self.Y+=py
        self.rect.center=(self.X+px,self.Y+py)
        self.SURFACE.blit(rotation_ship_image,self.rect)
    def damage(self,x):
        self.life-=x
        self.bar.bar_draw(self.max_life,self.life,self.X,self.Y)
    def bar_d(self):
        self.bar.bar_alone(self.X,self.Y)
        #color_change(self.img,pygame.Color(128,128,128))
    def boss_zombie_move(self,xv,V):
        if V==1:self.Y+=xv
        elif V==2:self.X-=xv
        elif V==3:self.X+=xv
        elif V==4:self.Y-=xv
        self.rect.center=(self.X,self.Y)
    def damage_stack(self):
        D=self.ds
        self.ds=0
        return D
















    

import sys
import random
import pygame
import time
import math
import stamina_code as sc

import boss_code as bc
#from math import factorial as f
#from pyc import *
#import serial
#from tkinter import *
#from tkinter import messagebox
#from pygame.locals import QUIT,KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,Rect,MOUSEBUTTONDOWN,K_SPACE,MOUSEBUTTONUP
def arduino_write(A):
    input_str=A
    input_str = input_str.encode('utf-8')
    ser.write(input_str)
def color_change(img,color):
    w,h=img.get_size()
    r,g,b,_=color
    for x in range(w):
        for y in range(h):
            a=img.get_at((x,y))[3]
            img.set_at((x,y),pygame.Color(r,g,b,a))
class zombie_life():
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
class zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img=pygame.image.load("z0.png").convert_alpha()
        self.img=pygame.transform.scale(self.img,(69,60))#(56,60))
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
        self.life=20#20
        self.max_life=20#20
        self.bar=zombie_life(self.max_life)
        self.img_size_idx=0
        self.lisi=0
        self.ig_idx_move=1
        self.img_size=[[69,60],[231*60/182,60.66666666666667],[240*60/182,60.66666666666667],[244*60/182,60.66666666666667],[253*60/182,60.66666666666667]]
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
        if math.sqrt(abs(450-self.X)**2+abs(450-self.Y)**2)>80:
            self.X+=math.sin(math.radians(FG+90))*1
            self.Y+=math.cos(math.radians(FG+90))*1
            self.ig_idx_move=1
            #self.lisi=self.img_size_idx
            self.img_size_idx=0
            if self.lisi==0:
                self.img=pygame.image.load("z"+str(self.img_size_idx//3)+".png").convert_alpha()
                self.img=pygame.transform.scale(self.img,(self.img_size[self.img_size_idx//3][0],self.img_size[self.img_size_idx//3][1]))#(56,60))
                self.lisi=1
        else:
            self.lisi=0
            R=self.img_size[self.img_size_idx//3][0]-self.img_size[0][0]
            px=math.sin(math.radians(FG+90))*R/2#*0.5#*0#.001#*1.5#*2
            py=math.cos(math.radians(FG+90))*R/2
            if self.ig_idx_move==1:
                #*0.5#*0#.001#*1.5
                #self.lisi=self.img_size_idx
                self.img_size_idx+=1
                if self.img_size_idx//3>=5:self.img_size_idx=3*5;self.ig_idx_move=-1;A.life-=3
            if self.ig_idx_move==-1:
                #self.lisi=self.img_size_idx
                self.img_size_idx-=1
                if self.img_size_idx//3<0:self.img_size_idx=0;self.ig_idx_move=1
            #if self.img_size_idx//100<0 or self.img_size_idx//5>=5:
                #print(self.img_size_idx%100)
            #print(A.life)
            if A.life<=0:GAME_OVER()
            self.img=pygame.image.load("z"+str(self.img_size_idx//3)+".png").convert_alpha()
            self.img=pygame.transform.scale(self.img,(self.img_size[self.img_size_idx//3][0],self.img_size[self.img_size_idx//3][1]))#(56,60))
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
class player_life_draw():
    #global SURFACE
    def __init__(self):
        #global SURFACE
        self.background_img=pygame.image.load("background_hp.png")
        self.w=345.5
        self.h=41
        self.w1=339.5
        self.h1=36
        self.background_img=pygame.transform.scale(self.background_img,(self.w,self.h))#(56,60))
        self.img=pygame.image.load("p_hp.png")
        self.p_img=pygame.transform.scale(self.img,(self.w1,self.h1))#(56,60))
        self.rect=self.background_img.get_rect()
        self.rect.center=(450,860)
        self.SURFACE=SURFACE
    def draw(self,mlife,life):
        self.SURFACE.blit(self.background_img,self.rect)
        self.p_img=pygame.transform.scale(self.img,((self.w1/mlife*life),self.h1))#(56,60))
        self.SURFACE.blit(self.p_img,(450-self.w/2+(self.w-self.w1)/2,860-self.h/2+(self.h-self.h1)/2))
class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_oj=[pygame.image.load("p"+str(i)+".png").convert_alpha()for i in range(6)]
        self.img_sl=[[56,60],[230*56/195,206*60/208],[250*56/195,206*60/208],[258*56/195,206*60/208],[263*56/195,206*60/208],[275*56/195,206*60/208]]
        for i in range(6):self.img_oj[i]=pygame.transform.scale(self.img_oj[i],self.img_sl[i])
        self.img=self.img_oj[0]
        self.mask=pygame.mask.from_surface(self.img)
        self.gun_img=pygame.image.load("gun_img.png").convert_alpha()
        self.gun_img=pygame.transform.scale(self.gun_img,(360*(56/195),188*(60/208)))
        self.rect=self.img.get_rect()
        self.rect.center=(450,450)
        self.img_number=0
        self.mouse_angle=0
        self.SURFACE=SURFACE
        self.langle=0
        self.X=450
        self.Y=450
        self.img_idx=0
        self.lisi=0
        self.img_move=1
        self.life=100#000#100
        self.mlife=100#000
        self.stamina_dt=300
        self.stamina_delay=0
        self.stamina_item_cnt=0
        self.life_draw=player_life_draw()
    def pld(self):
        self.life_draw.draw(self.mlife,self.life)
    def mouse_angle_update(self):
        global A
        Mouse=pygame.mouse.get_pos()
        mouse_x=Mouse[0]
        mouse_y=Mouse[1]
        self.mouse_angle= math.pi- math.atan2(mouse_x-450, mouse_y-450)
        rotation_ship_image= pygame.transform.rotate(self.img,-(int(math.degrees(self.mouse_angle)))+90)
        self.ship_image_pos= rotation_ship_image.get_rect()
        AG=-(int(math.degrees(self.mouse_angle)))+90
        if A.img!=A.gun_img:
            R=A.img_sl[A.img_idx//3][0]-A.img_sl[0][0]
            px=math.sin(math.radians(AG+90))*R/2#*0.5#*0#.001#*1.5#*2
            py=math.cos(math.radians(AG+90))*R/2
        else:
            R=360*(56/195)-56
            px=math.sin(math.radians(AG+90))*R/2#*0.5#*0#.001#*1.5#*2
            py=math.cos(math.radians(AG+90))*R/2
        self.ship_image_pos.center=(450+px,450+py)
        self.SURFACE.blit(rotation_ship_image,self.ship_image_pos)
    def arduino_angle_update(self,x,y):
        mouse_x=x
        mouse_y=y
        self.mouse_angle= math.pi- math.atan2(mouse_x-510, mouse_y-505)
        U=-(int(math.degrees(self.mouse_angle)))+180
        self.langle=U
        rotation_ship_image= pygame.transform.rotate(self.img,U)
        self.ship_image_pos= rotation_ship_image.get_rect()
        AG=U
        if A.img!=A.gun_img:
            R=A.img_sl[A.img_idx//3][0]-A.img_sl[0][0]
            px=math.sin(math.radians(AG+90))*R/2#*0.5#*0#.001#*1.5#*2
            py=math.cos(math.radians(AG+90))*R/2
        else:
            R=360*(56/195)-56
            px=math.sin(math.radians(AG+90))*R/2#*0.5#*0#.001#*1.5#*2
            py=math.cos(math.radians(AG+90))*R/2
        self.ship_image_pos.center=(450+px,450+py)
        self.SURFACE.blit(rotation_ship_image,self.ship_image_pos)
    def change_img(self,x):
        return
        self.img=pygame.image.load("player_bag_"+str(x)+".png").convert_alpha()
        self.img=pygame.transform.scale(self.img,bagsize[x])#(56,60))
        self.img_ca=self.img.convert_alpha()
        self.rect=self.img.get_rect()
        self.rect.center=(450,450)
        self.img_number=x
    def arduino_last_angle(self):
        rotation_ship_image= pygame.transform.rotate(self.img,self.langle)
        self.ship_image_pos= rotation_ship_image.get_rect()
        self.ship_image_pos.center=(450,450)
        self.SURFACE.blit(rotation_ship_image,self.ship_image_pos)
class bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img=pygame.image.load("bullet.png")
        self.img=pygame.transform.scale(self.img,(10,10))#(56,60))
        self.mask=pygame.mask.from_surface(self.img)
        self.mouse_angle=0
        self.SURFACE=SURFACE
        self.x=450
        self.y=450
        self.x1=450
        self.y1=450
        self.x2=450
        self.y2=450
        self.xd=0
        self.yd=0
        self.cnt=0
        self.delete=0
        self.delay=0
        self.rect=self.img.get_rect()
        self.rect.center=(450,450)
    def arduino_shot(self,x):
        #Mouse=pygame.mouse.get_pos()
        #mouse_x=Mouse[0]
        #mouse_y=Mouse[1]
        #self.mouse_angle= math.pi- math.atan2(mouse_x-450, mouse_y-450)
        #FG=-(int(math.degrees(self.mouse_angle)))+90
        rt=pygame.transform.rotate(self.img,x+90)
        self.xd=math.sin(math.radians(x+90))#FG+90))
        self.yd=math.cos(math.radians(x+90))#FG+90))
        self.rect=rt.get_rect()
        self.rect.center=(450,450)
        self.SURFACE.blit(rt,self.rect)
    def mouse_shot(self):
        Mouse=pygame.mouse.get_pos()
        mouse_x=Mouse[0]
        mouse_y=Mouse[1]
        self.mouse_angle= math.pi- math.atan2(mouse_x-450, mouse_y-450)
        FG=-(int(math.degrees(self.mouse_angle)))+90
        rt=pygame.transform.rotate(self.img,FG)
        self.xd=math.sin(math.radians(FG+90))
        self.yd=math.cos(math.radians(FG+90))
        self.rect=rt.get_rect()
        self.rect.center=(450,450)
        self.SURFACE.blit(rt,self.rect)
    def shot_move(self):
        if self.delete==0:
            self.x+=self.xd*5
            self.y+=self.yd*5
            if self.cnt>=2:
                self.x1+=self.xd*5
                self.y1+=self.yd*5
            if self.cnt>=4:
                self.x2+=self.xd*5
                self.y2+=self.yd*5
            self.cnt+=1
            if self.cnt>=310:self.delete=1
            elif self.cnt>=18:
                self.rect.center=(self.x,self.y)#int(self.x),int(self.y))
                #self.SURFACE.blit(self.rt,self.ship_image_pos)
                self.img.set_alpha(256)
                self.SURFACE.blit(self.img,self.rect)#(self.x,self.y))
                if self.cnt>=20:self.img.set_alpha(200);self.SURFACE.blit(self.img,self.rect)#(self.x1,self.y1))
                if self.cnt>=22:self.img.set_alpha(150);self.SURFACE.blit(self.img,self.rect)#(self.x2,self.y2))
class gun_object(pygame.sprite.Sprite):
    def __init__(self,X,Y,fg):
        pygame.sprite.Sprite.__init__(self)
        if fg==0:
            self.img=pygame.image.load("gun\AK47_item.png").convert_alpha()
            self.obj_name="AK47"
            self.img=pygame.transform.scale(self.img,(70,70))#(56,60))
            self.mask=pygame.mask.from_surface(self.img)
        else:
            self.img=pygame.image.load("gun\seven.png").convert_alpha()
            self.obj_name="7.62mm"
            self.img=pygame.transform.scale(self.img,(45,45))#(56,60))
            self.mask=pygame.mask.from_surface(self.img)
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
        if x==1:self.Y+=3;A.Y+=3#;zombie_move(0.2,1)
        elif x==2:self.X-=3;A.X-=3#;zombie_move(0.2,2)
        elif x==3:self.X+=3;A.X+=3#;zombie_move(0.2,3)
        elif x==4:self.Y-=3;A.Y-=3#;zombie_move(0.2,4)
        self.rect.center=(self.X,self.Y)
        #print("##",self.X,self.Y)
class boost_item(pygame.sprite.Sprite):
    def __init__(self,fg):
        pygame.sprite.Sprite.__init__(self)
        X=random.randint(40,860)
        Y=random.randint(40,860)
        if fg==0:
            self.img=pygame.image.load("player_bag_0.png").convert_alpha()
            self.obj_name="drink"
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


def zombie_move(xv,V):
    global zst
    for i in range(len(zst)):
        if V==1:zst[i].Y+=xv
        elif V==2:zst[i].X-=xv
        elif V==3:zst[i].X+=xv
        elif V==4:zst[i].Y-=xv
def text_draw(inp):
    snt=2*len(inp)
    #for i in range(len(inp)):

    #    if ord(inp[i])>=12000:snt+=2
    #    else:snt+=1
    myFont=pygame.font.SysFont('malgungothicsemilight',20)
    TEXT0="┏     "+" "*snt+"     ┓"
    TEXT1=" "*7+inp+" "*7
    TEXT2="┖     "+" "*snt+"     ┚"
    #print(TEXT)
    text_Title=myFont.render(TEXT0,True,(255,255,255))
    text_Rect=text_Title.get_rect()
    text_Rect.center=(450,350)
    SURFACE.blit(text_Title,text_Rect)
    text_Title=myFont.render(TEXT1,True,(255,255,255))
    text_Rect=text_Title.get_rect()
    text_Rect.center=(450,370)
    SURFACE.blit(text_Title,text_Rect)
    text_Title=myFont.render(TEXT2,True,(255,255,255))
    text_Rect=text_Title.get_rect()
    text_Rect.center=(450,390)
    SURFACE.blit(text_Title,text_Rect)
def crash():
    global crash_idx,bt_crash_idx,asd,sa_crash_idx
    for i in range(len(gun_item_stack)):
        if pygame.sprite.collide_mask(gun_item_stack[i],A):#gun_item_stack[i+1]):
            if asd=="keyboard":
                text_draw("F 키로 AK47 줍기")
            #print("ADFASDASD")
            crash_idx=i
            bt_crash_idx=-1
            return
    crash_idx=-1
    for i in range(len(bullet_item_stack)):
        if pygame.sprite.collide_mask(bullet_item_stack[i][0],A):#gun_item_stack[i+1]):
            if asd=="keyboard":
                text_draw("F 키로 7.62탄 줍기")
            #print("ADFASDASD")
            bt_crash_idx=i
            return
    bt_crash_idx=-1
    for i in range(len(stamina_item_stack)):
        if pygame.sprite.collide_mask(stamina_item_stack[i],A):
            if asd=="keyboard":
                text_draw("F 키로 붕대 줍기")
            sa_crash_idx=i
            return
    sa_crash_idx=-1
            
def DRAW():
    for i in range(len(gun_item_stack)):gun_item_stack[i].draw()
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].draw()
    for i in range(len(stamina_item_stack)):stamina_item_stack[i].draw()
def left():
    #print("ASD")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(3)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(3)
    #for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(3)
    for i in range(len(stamina_item_stack)):stamina_item_stack[i].keyboard_move(3)
    for i in range(len(boss_stack)):boss_stack[i][0].boss_zombie_move(3,3)
    zombie_move(2,3)
def right():
    #print("ASDD")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(2)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(2)
    #for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(2)
    for i in range(len(stamina_item_stack)):stamina_item_stack[i].keyboard_move(2)
    for i in range(len(boss_stack)):boss_stack[i][0].boss_zombie_move(3,2)
    zombie_move(2,2)
def up():
    #print("!@#")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(1)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(1)
    #for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(1)
    for i in range(len(stamina_item_stack)):stamina_item_stack[i].keyboard_move(1)
    for i in range(len(boss_stack)):boss_stack[i][0].boss_zombie_move(3,1)
    zombie_move(2,1)
def down():
    #print("DFG")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(4)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(4)
    #for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(4)
    for i in range(len(stamina_item_stack)):stamina_item_stack[i].keyboard_move(4)
    for i in range(len(boss_stack)):boss_stack[i][0].boss_zombie_move(3,4)
    zombie_move(2,4)
c_d=[pygame.image.load("bandage_cnt.png")]
c_d[0]=pygame.transform.scale(c_d[0],(120,50))
def cnt_draw(x):
    if x==0:
        asd=0
        SURFACE.blit(c_d[0],(650,820))
        myFont=pygame.font.SysFont('malgungothicsemilight',20)
        text_Title=myFont.render(str(A.stamina_item_cnt),True,(255,255,255))
        text_Rect=text_Title.get_rect()
        text_Rect.center=(720,843)
        SURFACE.blit(text_Title,text_Rect)
    #A.stamina_item_cnt
class gun:
    def __init__(self):
        self.reloading=[250]#250]
        self.delay=[10]#0]
        self.bulletcnt=[30]
        self.gun_name=["AK47"]
        self.left_bulletcnt=[0]
        self.user_bulletcnt=[-1,-1]
        self.user_gun_number=[-1,-1]
        self.user_delay=[-1,-1]
        self.user_reloading=[[-1,0],[-1,0]]
        self.select=0
def reloading():
    global GUN
    ga=GUN.user_gun_number
    gs=ga[GUN.select]
    if gs==-1:return
    hand=GUN.select
    asdf=0
    if GUN.gun_name[gs]=="AK47":asdf=0
    if GUN.left_bulletcnt[asdf]>0 and GUN.user_reloading[hand][1]==0 and GUN.user_bulletcnt[hand]!=GUN.bulletcnt[gs]:
        print("reloading...")
        GUN.user_reloading[hand][1]=1
        GUN.user_reloading[hand][0]=GUN.reloading[gs]
def pick_up():
    global bullet_item_stack,gun_item_stack
    global crash_idx,bt_crash_idx,sa_crash_idx
    #print("ASDASD",crash_idx)
    if crash_idx!=-1:
        if GUN.user_gun_number[0]==-1:
            GUN.user_gun_number[0]=0
            A.img=A.gun_img
            #GUN.user_reloading[0][0]=GUN.reloading[GUN.user_gun_number[0]]
            #GUN.user_reloading[0][1]=1
            GUN.user_bulletcnt[0]=0#GUN.bulletcnt[GUN.user_gun_number[0]]
            GUN.user_delay[0]=GUN.delay[GUN.user_gun_number[0]]
            if GUN.select==0:
                asdf=0
                if GUN.gun_name[GUN.user_gun_number[0]]=="AK47":asdf=0
                if GUN.left_bulletcnt[asdf]>0:
                    print("reloading...")
                    ga=GUN.user_gun_number
                    gs=ga[0]
                    GUN.user_reloading[GUN.select][1]=1
                    GUN.user_reloading[GUN.select][0]=GUN.reloading[gs]
            gun_item_stack.pop(crash_idx)
        elif GUN.user_gun_number[1]==-1:
            GUN.user_gun_number[1]=0
            A.img=A.gun_img
            #GUN.user_reloading[1][0]=GUN.reloading[GUN.user_gun_number[1]]
            #GUN.user_reloading[1][1]=1
            GUN.user_bulletcnt[1]=0#GUN.bulletcnt[GUN.user_gun_number[1]]
            GUN.user_delay[1]=GUN.delay[GUN.user_gun_number[1]]
            if GUN.select==1:
                asdf=0
                if GUN.gun_name[GUN.user_gun_number[1]]=="AK47":asdf=0
                if GUN.left_bulletcnt[asdf]>0:
                    print("reloading...")
                    ga=GUN.user_gun_number
                    gs=ga[1]
                    GUN.user_reloading[GUN.select][1]=1
                    GUN.user_reloading[GUN.select][0]=GUN.reloading[gs]
            gun_item_stack.pop(crash_idx)
        else:
            print("full")
    if bt_crash_idx!=-1:
        if bullet_item_stack[bt_crash_idx][1]==7.62:
            GUN.left_bulletcnt[0]+=bullet_item_stack[bt_crash_idx][2]
        #print(GUN.user_bulletcnt[GUN.select])
        if GUN.user_bulletcnt[GUN.select]!=-1:
            ga=GUN.user_gun_number
            gs=ga[GUN.select]
            #print("#",GUN.user_reloading[GUN.select][1])
            if GUN.user_reloading[GUN.select][1]==0 and GUN.user_bulletcnt[GUN.select]==0:
                asdf=0
                if GUN.gun_name[gs]=="AK47":asdf=0
                #print(GUN.left_bulletcnt[asdf],GUN.user_reloading[GUN.select][1])
                if GUN.left_bulletcnt[asdf]>0:#GUN.user_reloading[GUN.select][1]==0:
                    print("reloading...")
                    GUN.user_reloading[GUN.select][1]=1
                    GUN.user_reloading[GUN.select][0]=GUN.reloading[gs]
        #print(GUN.left_bulletcnt)
        bullet_item_stack.pop(bt_crash_idx)
    if sa_crash_idx!=-1:
        A.stamina_item_cnt+=3
        stamina_item_stack.pop(sa_crash_idx)
        #print(A.stamina_item_cnt)
def arduino():
    global ser,F_on
    global bulletm,keys,R_on
    global bullet_item_stack,gun_item_stack
    global A
    #print("!@#")
    if ser.readable():
        #print("ZXC")
        res=ser.readline()
        ready=res.decode()[:len(res)-2]
        ready=ready.split()
        if len(ready)!=8:return
        ready=[int(ready[x])for x in range(len(ready))]#1,2,3,4:조이스틱,5,6,7,8:총쏘기,제장전,줍기,ㅁㄴㅇ
        #print("XZ")
        #move
        ux=503#510 500
        uy=519#505 518
        #print("ASDASDASD")
        if ux+10<ready[2] or ready[2]<ux-10:ux=ready[2]
        if uy+10<ready[3] or ready[3]<uy-10:uy=ready[3]
        #print("ASD")
        #print(ready[2],ready[3],ux,uy)
        if ux!=503:
            if ux<503:down()
            if ux>503:up()
        if uy!=519:
            if uy<519:left()
            if uy>519:right() 
        if ready[6]==1:
            if F_on==0:pick_up();F_on=1
        else:F_on=0
        if ready[5]==1:
            if R_on==0:reloading();R_on=1
        else:R_on=0
        if ready[4]==1:
            #print("ASDE")
            ga=GUN.user_gun_number
            gs=ga[GUN.select]
            hand=GUN.select
            if gs!=-1:
                if A.lisi==0:A.img_idx=0;A.img_move=1;A.lisi=1#A.img_oj[0]
                asdf=0
                if GUN.gun_name[gs]=="AK47":asdf=0
                if GUN.left_bulletcnt[asdf]==0 and GUN.user_bulletcnt[hand]==0:
                    text_draw("총알이 없습니다")
                    ASD=chr(0x31)
                    ASD=ASD.encode()
                    ser.write(ASD)
                    
                    #print("Don't have bullet")
                else:
                    #print(GUN.user_delay[hand],GUN.user_reloading[hand][1],hand)
                    #print(ga,gs,GUN.mousedelay[gs],GUN.bulletcnt[gs],GUN.reloading[gs])
                    if GUN.user_delay[hand]==0 and GUN.user_reloading[hand][1]==0 and GUN.user_bulletcnt[hand]>0:
                        #print("#")
                        er=bullet()
                        er.arduino_shot(A.langle)
                        bulletm.append(er)
                        GUN.user_delay[hand]=GUN.delay[gs]
                        GUN.user_bulletcnt[hand]-=1
                        if GUN.user_bulletcnt[hand]==0:
                            if GUN.left_bulletcnt[asdf]>0:
                                print("reloading...")
                                GUN.user_reloading[hand][1]=1
                                GUN.user_reloading[hand][0]=GUN.reloading[gs]
            else:
                A.lisi=0
                if A.img_move==1:
                    A.img_idx+=1
                    if A.img_idx//3>=6:
                        A.img_idx=18
                        A.img_move=-1
                if A.img_move==-1:
                    A.img_idx-=1
                    if A.img_idx//3<0:
                        A.img_idx=0
                        A.img_move=1
                A.img=A.img_oj[A.img_idx//3]
                if A.img_idx//3==5:
                    for i in range(len(zst)):
                        if math.sqrt(abs(zst[i].X-450)**2+abs(zst[i].Y-450)**2)<=85:
                            zst[i].damage(0.3)
                            if zst[i].life<=0:
                                zst.pop(i)
                            break
                    for i in range(len(boss_stack)):
                        if math.sqrt(abs(boss_stack[i][0].X-450)**2+abs(boss_stack[i][0].Y-450)**2)<=100:
                            boss_stack[i][0].damage(0.3)
                            if boss_stack[i][0].life<=0:
                                boss_stack.pop(i)
                            break
                #-(int(math.degrees(self.mouse_angle)))+90
        else:
            if A.lisi==0:A.img_idx=0;A.img_move=1;A.lisi=1;A.img=A.img_oj[0]
        if ready[7]==1:
            if A.stamina_item_cnt>0 and A.life<100:
                if A.stamina_delay==0:
                    A.stamina_item_cnt-=1
                    A.life=min(100,A.life+10)
                    #print(A.stamina_item_cnt)
                    A.stamina_delay=A.stamina_dt
        rx=511#510 500
        ry=505#505 518
        #print("ASDASDASD")
        if rx+5<ready[0] or ready[0]<rx-5:rx=ready[0]
        if ry+5<ready[1] or ready[1]<ry-5:ry=ready[1]
        #print("ASD")
        #print(ready[0],ready[1],rx,ry)
        if rx!=511 or ry!=505:A.arduino_angle_update(rx,ry)
        else:A.arduino_last_angle()
def keyboard():
    global bulletm,keys,F_on,R_on,A,zst
    global bullet_item_stack,gun_item_stack
    if keys[pygame.K_7]:
        if A.stamina_item_cnt>0 and A.life<100:
            if A.stamina_delay==0:
                A.stamina_item_cnt-=1
                A.life=min(100,A.life+10)
                #print(A.stamina_item_cnt)
                A.stamina_delay=A.stamina_dt
    if keys[pygame.K_w]:up()
    if keys[pygame.K_d]:right()
    if keys[pygame.K_a]:left()
    if keys[pygame.K_s]:down()
    #if keyboard.is_pressed("f")
    if keys[pygame.K_f]:
        if F_on==0:pick_up();F_on=1
    else:F_on=0
    if keys[pygame.K_r]:
        if R_on==0:reloading();R_on=1
    else:R_on=0
    #print(F_on)
    #print(pygame.mouse.get_pressed())
    if pygame.mouse.get_pressed()[0]:
        #print("ASDE")
        ga=GUN.user_gun_number
        gs=ga[GUN.select]
        hand=GUN.select
        if gs!=-1:
            if A.lisi==0:A.img_idx=0;A.img_move=1;A.lisi=1#A.img_oj[0]
            asdf=0
            if GUN.gun_name[gs]=="AK47":asdf=0
            if GUN.left_bulletcnt[asdf]==0 and GUN.user_bulletcnt[hand]==0:
                text_draw("총알이 없습니다")
                #print("Don't have bullet")
            else:
                #print(GUN.user_delay[hand],GUN.user_reloading[hand][1],hand)
                #print(ga,gs,GUN.mousedelay[gs],GUN.bulletcnt[gs],GUN.reloading[gs])
                if GUN.user_delay[hand]==0 and GUN.user_reloading[hand][1]==0 and GUN.user_bulletcnt[hand]>0:
                    #print("#")
                    er=bullet()
                    er.mouse_shot()
                    bulletm.append(er)
                    GUN.user_delay[hand]=GUN.delay[gs]
                    GUN.user_bulletcnt[hand]-=1
                    if GUN.user_bulletcnt[hand]==0:
                        if GUN.left_bulletcnt[asdf]>0:
                            print("reloading...")
                            GUN.user_reloading[hand][1]=1
                            GUN.user_reloading[hand][0]=GUN.reloading[gs]
        else:
            A.lisi=0
            if A.img_move==1:
                A.img_idx+=1
                if A.img_idx//3>=6:
                    A.img_idx=18
                    A.img_move=-1
            if A.img_move==-1:
                A.img_idx-=1
                if A.img_idx//3<0:
                    A.img_idx=0
                    A.img_move=1
            A.img=A.img_oj[A.img_idx//3]
            if A.img_idx//3==5:
                for i in range(len(zst)):
                    if math.sqrt(abs(zst[i].X-450)**2+abs(zst[i].Y-450)**2)<=85:
                        zst[i].damage(0.3)
                        if zst[i].life<=0:
                            zst.pop(i)
                        break
                for i in range(len(boss_stack)):
                    if math.sqrt(abs(boss_stack[i][0].X-450)**2+abs(boss_stack[i][0].Y-450)**2)<=100:
                        boss_stack[i][0].damage(0.3)
                        if boss_stack[i][0].life<=0:
                            boss_stack.pop(i)
                        break
            #-(int(math.degrees(self.mouse_angle)))+90
    else:
        if A.lisi==0:A.img_idx=0;A.img_move=1;A.lisi=1;A.img=A.img_oj[0]
            
                
    #pygame.draw.circle(SURFACE,(251,206,177),(A.x,A.y),40)
    #A.img=pygame.transform.rotate(A.img,angle-A.mouse_angle)
    #A.angle=angle
    #print(angle,A.angle)
    A.mouse_angle_update()
def check(x,y):
    for g in range(len(bullet_item_stack)):
        posx=bullet_item_stack[g][0].X
        posy=bullet_item_stack[g][0].Y
        if math.sqrt(abs(posx-x)**2+abs(posy-y)**2)<75:return 0
    for g in range(len(gun_item_stack)):
        posx=gun_item_stack[g].X
        posy=gun_item_stack[g].Y
        if math.sqrt(abs(posx-x)**2+abs(posy-y)**2)<75:return 0
    for g in range(len(stamina_item_stack)):
        posx=stamina_item_stack[g].X
        posy=stamina_item_stack[g].Y
        if math.sqrt(abs(posx-x)**2+abs(posy-y)**2)<75:return 0
    return 1
def bullet_text():
    ga=GUN.user_gun_number
    gs=ga[GUN.select]
    hand=GUN.select
    if gs!=-1:
        asdf=0
        myFont=pygame.font.SysFont('malgungothicsemilight',50)
        if GUN.gun_name[gs]=="AK47":asdf=0
        TEXT0=str(GUN.user_bulletcnt[hand])
        #TEXT1=" "*7+inp+" "*7
        #TEXT2="┖     "+" "*snt+"     ┚"
        #print(TEXT)
        text_Title=myFont.render(TEXT0,True,(255,255,255))
        text_Rect=text_Title.get_rect()
        text_Rect.center=(450,800)
        myFont=pygame.font.SysFont('malgungothicsemilight',30)
        SURFACE.blit(text_Title,text_Rect)
        TEXT0=str(GUN.left_bulletcnt[asdf])
        #TEXT1=" "*7+inp+" "*7
        #TEXT2="┖     "+" "*snt+"     ┚"
        #print(TEXT)
        text_Title=myFont.render(TEXT0,True,(255,255,255))
        text_Rect=text_Title.get_rect()
        text_Rect.center=(530,805)
        SURFACE.blit(text_Title,text_Rect)
#main
def before_start():
    global asd,ser
    intro=pygame.image.load("intro.png")
    intro=pygame.transform.scale(intro,(900,900))
    start=pygame.image.load("start.png")
    start=pygame.transform.scale(start,(200,100))
    FPSCLOCK.tick(10)
    #print("SDFSDF")
    while 1:
        #print("AASD")
        SURFACE.fill((255,255,255))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:break
        SURFACE.blit(intro,(0,0))
        Mouse=pygame.mouse.get_pos()
        if 350<=Mouse[0]<=550 and 550<=Mouse[1]<=650:
            st=pygame.transform.scale(start,(220,120))
            SURFACE.blit(st,(340,540))
            if pygame.mouse.get_pressed()[0]:
                #print("SDFSDFSDFSFDSDF")
                break
        else:
            st=pygame.transform.scale(start,(200,100))
            SURFACE.blit(st,(350,550))
        
        pygame.display.update()
        #FPSCLOCK.tick(10)
    cs=0
    no=0
    left=0
    right=0
    try:
        ser=serial.Serial('COM4',115200)
        #print("asd")
    except:
        no=1
    keyboard_img=pygame.image.load("keyboard.png")
    keyboard_img=pygame.transform.scale(keyboard_img,(320,160))
    cr_img=pygame.image.load("game_controller.png")
    cr_img=pygame.transform.scale(cr_img,(160,160))
    while 1:
        SURFACE.fill((0,0,0))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:break
        #self.rect=self.img.get_rect()
        #self.rect.center=(self.X,self.Y)#x=self.X
        #self.SURFACE.blit(self.img,self.rect)#(self.rect.centerx,self.rect.centerx))
        kr=keyboard_img.get_rect()
        kr.center=(250,450)#x=self.X
        SURFACE.blit(keyboard_img,kr)#(self.rect.centerx,self.rect.centerx))
        kr=cr_img.get_rect()
        kr.center=(650,450)#x=self.X
        SURFACE.blit(cr_img,kr)#(self.rect.centerx,self.rect.centerx))
        if no==1:
            X_img=pygame.image.load("X.png")
            X_img=pygame.transform.scale(X_img,(215,215))
            kr=cr_img.get_rect()
            kr.center=(650-27.5,450-27.5)#x=self.X
            SURFACE.blit(X_img,kr)#(self.rect.centerx,self.rect.centerx))
        myFont=pygame.font.SysFont('malgungothicsemilight',40)
        text_Title=myFont.render("KEYBOARD",True,(255,255,255))
        text_Rect=text_Title.get_rect()
        text_Rect.center=(250,570)
        SURFACE.blit(text_Title,text_Rect)
        text_Title=myFont.render("ARDUINO",True,(255,255,255))
        text_Rect=text_Title.get_rect()
        text_Rect.center=(650,570)
        SURFACE.blit(text_Title,text_Rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if cs==1 and no==0:
                asd="arduino"
                return
            if cs==0:
                asd="keyboard"
                return
        if keys[pygame.K_LEFT] and left==0:
            cs-=1
            #print("ASDA")
            if cs<0:cs=1
            left=1
        else:
            left=0
        if keys[pygame.K_RIGHT] and right==0:
            cs+=1
            #print("@S")
            if cs>1:cs=0
            right=1
        else:
            right=0
        #print(cs)
        if cs==0:
            pygame.draw.rect(SURFACE,(255,255,0), [60,300,380,390],10)
        else:
            pygame.draw.rect(SURFACE,(255,255,0), [460,300,380,390],10)
        pygame.display.update()
        FPSCLOCK.tick(10)
pygame.init()
FPSCLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((900,900))
#print("!")
bagsize=[[56,60],[69,60],[73,60],[79,60]]
asd=""
ser=0
bulletm=[]
boss_stack=[]
gun_item_stack=[]
bullet_item_stack=[]
boost_item_stack=[]
stamina_item_stack=[]
bt_crash_idx=-1
crash_idx=-1
sa_crash_idx=-1
A=0
GUN=0
SCORE=0
zst=[]
keys=0
b_cnt=0
def GAME_OVER():
    global SCORE
    gameover=pygame.image.load("GAMEOVER.png")
    gameover=pygame.transform.scale(gameover,(681,108))
    RE=pygame.image.load("RE.png")
    Z=0
    myFont=pygame.font.SysFont('malgungothicsemilight',50)
    text_Title=myFont.render("YOUR SCORE IS "+str(SCORE),True,(255,255,255))
    text_Rect=text_Title.get_rect()
    text_Rect.center=(450,450)
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:break
        SURFACE.fill((0,0,0))
        Mouse=pygame.mouse.get_pos()
        SURFACE.blit(gameover,(219/2,120))
        SURFACE.blit(text_Title,text_Rect)
        if 341<=Mouse[0]<=559 and 600<=Mouse[1]<=704:
            Z=pygame.transform.scale(RE,(228,114))
            SURFACE.blit(Z,(336,595))
            if pygame.mouse.get_pressed()[0]:
                GAME_START()
        else:
            Z=pygame.transform.scale(RE,(218,104))
            SURFACE.blit(Z,(341,600))
        pygame.display.update()
def GAME_START():
    global boss_stack,boost_item_stack,gun_item_stack,sa_crash_idx,crash_idx,zst
    global bulletm,stamina_item_stack,bullet_item_stack,bt_crash_idx,A,GUN,keys,SCORE
    before_start()
    bulletm=[]
    A=player()
    zst=[]
    boss_stack=[[bc.boss_zombie(),0]]
    for i in range(5):zst.append(zombie())
    col=0
    GUN=gun()
    rm=1#andom.randint(3,7)
    gun_item_stack=[]
    bullet_item_stack=[]
    boost_item_stack=[]
    stamina_item_stack=[]
    b_cnt=0
    SCORE=0
    #for i in range(5):boost_item_stack.append(boost_item(0))
    crash_idx=-1
    bt_crash_idx=-1
    sa_crash_idx=-1
    F_on=0
    R_on=0
    #print(asd)
    for i in range(rm):
        while 1:
            X=random.randint(40,860)
            Y=random.randint(40,860)
            if check(X,Y)==1:
                gun_item_stack.append(gun_object(X,Y,0))
                break
    rm1=random.randint(rm,rm+6)
    for i in range(rm1):
        while 1:
            X=random.randint(40,860)
            Y=random.randint(40,860)
            if check(X,Y)==1:
                bullet_item_stack.append([gun_object(X,Y,1),7.62,60])
                break
    for i in range(10):
        while 1:
            X=random.randint(40,860)
            Y=random.randint(40,860)
            if check(X,Y)==1:
                stamina_item_stack.append(sc.stamina_item(X,Y))
                break
    #zxczxczxczc=pygame.image.load("keyboard.png")
    while 1:
        #print(1)
        col+=1
        b_cnt+=1
        if b_cnt%500==0:boss_stack.append([bc.boss_zombie(),0])
        if col%300==0:zst.append(zombie())#300
        SURFACE.fill((72,105,13))
        #for g in range(len(boost_item_stack)):boost_item_stack[g].draw()
        #print(A.X,A.Y)
        #for event in pygame.event.get():
        DRAW()

        event = pygame.event.poll()
        if event.type == pygame.QUIT:break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_0]:A.change_img(0)
        if keys[pygame.K_1]:A.change_img(1)
        if keys[pygame.K_2]:A.change_img(2)
        if keys[pygame.K_3]:A.change_img(3)
        ga=GUN.user_gun_number
        gs=ga[GUN.select]
        hand=GUN.select
        if gs!=-1:
            asdf=0
            if GUN.gun_name[gs]=="AK47":asdf=0
            if GUN.left_bulletcnt[asdf]>0 and GUN.user_reloading[hand][1]==1 and GUN.user_reloading[hand][0]>0:
                GUN.user_reloading[hand][0]-=1
                if GUN.user_reloading[hand][0]==0:
                    #if asd=="arduino":arduino_write(str(GUN.bulletcnt[gs][1])+"/"+str(GUN.bulletcnt[gs][1]))
                    print("finish")
                    GUN.user_reloading[hand][1]=0
                    if GUN.gun_name[gs]=="AK47":
                        zx=min(GUN.bulletcnt[gs]-GUN.user_bulletcnt[hand],GUN.left_bulletcnt[0])
                        GUN.user_bulletcnt[hand]+=zx
                        GUN.left_bulletcnt[0]-=zx
                        #print(GUN.left_bulletcnt[0])
                    GUN.user_delay[hand]=0
        if hand==0 and ga[0]!=-1 and GUN.user_delay[0]>0:GUN.user_delay[0]-=1
        if hand==1 and ga[1]!=-1 and GUN.user_delay[1]>0:GUN.user_delay[1]-=1
        #print(mousedelay)
        #print(asd)
        z=0
        for i in range(len(bulletm)):
            bulletob=bulletm[i-z]
            bulletob.shot_move()
            er=0
            for g in range(len(zst)):
                if pygame.sprite.collide_mask(bulletob,zst[g-er]):
                    zst[g-er].damage(2)
                    if zst[g-er].life<=0:
                        RAD=random.randint(1,3)
                        SCORE+=1
                        if RAD==1:
                            bullet_item_stack.append([gun_object(zst[g-er].X,zst[g-er].Y,1),7.62,random.randint(15,25)])
                        zst.pop(g);er+=1
                    bulletm.pop(i-z);z+=1;break
            #if bulletob.delete==1:bulletm.pop(i-z);z+=1
            er=0
            for g in range(len(boss_stack)):
                if pygame.sprite.collide_mask(bulletob,boss_stack[g-er][0]):
                    boss_stack[g-er][0].damage(2)
                    if boss_stack[g-er][0].life<=0:
                        SCORE+=5
                        bullet_item_stack.append([gun_object(zst[g-er].X,zst[g-er].Y,1),7.62,random.randint(20,35)])
                        RAD=random.randint(1,2)
                        if RAD==1:
                            stamina_item_stack.append(sc.stamina_item(X,Y+50))
                        boss_stack.pop(g);er+=1
                    bulletm.pop(i-z);z+=1;break
            if bulletob.delete==1:bulletm.pop(i-z);z+=1
        #SURFACE.blit(A.img,(422,420))
        crash()
        for i in range(len(boss_stack)):
            boss_stack[i][0].watch_player()
            boss_stack[i][0].bar_d()
            A.life-=boss_stack[i][0].damage_stack()
        for g in range(len(zst)):
            zst[g].watch_player()
            zst[g].bar_d()
        bullet_text()
        A.pld()
        #sc.f(zxczxczxczc)
        if A.stamina_delay>0:
            A.stamina_delay-=1
        cnt_draw(0)
        if asd=="keyboard":
            keyboard()
        if asd=="arduino":
            #print("CXVXCVXCV")
            arduino()
        pygame.display.update()
        if asd!="arduino":FPSCLOCK.tick(100)
        #else:FPSCLOCK.tick(1300)
GAME_START()

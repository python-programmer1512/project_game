import sys
import random
import pygame
import time
import math
#from pyc import *
import serial
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
        self.img_size=[[69,60],[231*60/182,60.66666666666667],[240*60/182,60.66666666666667],[244*60/182,60.66666666666667],[253*60/182,60.66666666666667]]
    def watch_player(self):
        #global A
        #self.img_size_idx+=1
        #if self.img_size_idx%300>=5:self.img_size_idx=0
        #.convert_alpha()
        #self.img=pygame.image.load("z"+str(self.img_size_idx%100)+".png")
        #self.img=pygame.transform.scale(self.img,(self.img_size[self.img_size_idx%100][0],self.img_size[self.img_size_idx%100][1]))#(56,60))
        self.angle=math.pi-math.atan2(self.X-450,self.Y-450)
        FG=-(int(math.degrees(self.angle)))-90#+90
        rotation_ship_image= pygame.transform.rotate(self.img,FG)
        self.rect= rotation_ship_image.get_rect()
        #A.
        #self.xd=math.sin(math.radians(FG+90))
        #self.yd=math.cos(math.radians(FG+90))
        if math.sqrt(abs(450-self.X)**2+abs(450-self.Y)**2)>70:
            self.X+=math.sin(math.radians(FG+90))*1
            self.Y+=math.cos(math.radians(FG+90))*1
        else:
            A.life-=0.3
            #print(A.life)
            if A.life<=0:sys.exit()
        self.rect.center=(self.X,self.Y)
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
        self.p_img=pygame.image.load("p_hp.png")
        self.p_img=pygame.transform.scale(self.p_img,(self.w1,self.h1))#(56,60))
        self.rect=self.background_img.get_rect()
        self.rect.center=(450,860)
        self.SURFACE=SURFACE
    def draw(self,mlife,life):
        self.SURFACE.blit(self.background_img,self.rect)
        self.p_img=pygame.transform.scale(self.p_img,((self.w1/mlife*life),self.h1))#(56,60))
        self.SURFACE.blit(self.p_img,(450-self.w/2+(self.w-self.w1)/2,860-self.h/2+(self.h-self.h1)/2))
class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img=pygame.image.load("player_bag_0.png").convert_alpha()
        self.img=pygame.transform.scale(self.img,bagsize[0])#(56,60))
        self.mask=pygame.mask.from_surface(self.img)
        self.rect=self.img.get_rect()
        self.rect.center=(450,450)
        self.img_number=0
        self.mouse_angle=0
        self.SURFACE=SURFACE
        self.langle=0
        self.X=450
        self.Y=450
        self.life=100#100
        self.mlife=100
        self.life_draw=player_life_draw()
    def pld(self):
        self.life_draw.draw(self.mlife,self.life)
    def mouse_angle_update(self):
        Mouse=pygame.mouse.get_pos()
        mouse_x=Mouse[0]
        mouse_y=Mouse[1]
        self.mouse_angle= math.pi- math.atan2(mouse_x-450, mouse_y-450)
        rotation_ship_image= pygame.transform.rotate(self.img,-(int(math.degrees(self.mouse_angle)))+90)
        self.ship_image_pos= rotation_ship_image.get_rect()
        self.ship_image_pos.center=(450,450)
        self.SURFACE.blit(rotation_ship_image,self.ship_image_pos)
    def arduino_angle_update(self,x,y):
        mouse_x=x
        mouse_y=y
        self.mouse_angle= math.pi- math.atan2(mouse_x-510, mouse_y-505)
        U=-(int(math.degrees(self.mouse_angle)))+180
        self.langle=U
        rotation_ship_image= pygame.transform.rotate(self.img,U)
        self.ship_image_pos= rotation_ship_image.get_rect()
        self.ship_image_pos.center=(450,450)
        self.SURFACE.blit(rotation_ship_image,self.ship_image_pos)
    def change_img(self,x):
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
            if self.cnt>=300:self.delete=1
            elif self.cnt>=8:
                self.rect.center=(self.x,self.y)#int(self.x),int(self.y))
                #self.SURFACE.blit(self.rt,self.ship_image_pos)
                self.img.set_alpha(256)
                self.SURFACE.blit(self.img,self.rect)#(self.x,self.y))
                if self.cnt>=10:self.img.set_alpha(200);self.SURFACE.blit(self.img,self.rect)#(self.x1,self.y1))
                if self.cnt>=12:self.img.set_alpha(150);self.SURFACE.blit(self.img,self.rect)#(self.x2,self.y2))
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
        if x==1:self.Y+=3;A.Y+=3;zombie_move(0.2,1)
        elif x==2:self.X-=3;A.X-=3;zombie_move(0.2,2)
        elif x==3:self.X+=3;A.X+=3;zombie_move(0.2,3)
        elif x==4:self.Y-=3;A.Y-=3;zombie_move(0.2,4)
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
    global crash_idx,bt_crash_idx,asd
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
def DRAW():
    for i in range(len(gun_item_stack)):gun_item_stack[i].draw()
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].draw()
def left():
    #print("ASD")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(3)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(3)
    for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(3)
def right():
    #print("ASDD")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(2)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(2)
    for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(2)
def up():
    #print("!@#")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(1)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(1)
    for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(1)
def down():
    #print("DFG")
    for i in range(len(gun_item_stack)):gun_item_stack[i].keyboard_move(4)
    for i in range(len(bullet_item_stack)):bullet_item_stack[i][0].keyboard_move(4)
    for i in range(len(boost_item_stack)):boost_item_stack[i].keyboard_move(4)
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
    global crash_idx,bt_crash_idx
    #print("ASDASD",crash_idx)
    if crash_idx!=-1:
        if GUN.user_gun_number[0]==-1:
            GUN.user_gun_number[0]=0
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
                asdf=0
                if GUN.gun_name[gs]=="AK47":asdf=0
                if GUN.left_bulletcnt[asdf]==0 and GUN.user_bulletcnt[hand]==0:print("Don't have bullet")
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
        #if ready[2]==1:
        #    ga=GUN.user_gun_number
        #    gs=ga[GUN.select]
        #    #print("#")
        #    #print(mousedelay[0][1]==0 and reloading[0][2]
        #    if GUN.mousedelay[gs][1]==0 and GUN.reloading[gs][2]==0:
        #        er=bullet()
        #        er.arduino_shot(A.langle)
        #        bulletm.append(er)
        #        GUN.mousedelay[gs][1]=GUN.mousedelay[gs][0]
        #        GUN.bulletcnt[0][1]-=1
        #        if GUN.bulletcnt[gs][1]==0:
        #            #arduino_write("reloading...")
        #            print("reloading...")
        #            GUN.reloading[gs][2]=1
        #            GUN.reloading[gs][1]=GUN.reloading[gs][0]
        #        #else:
        #        #    arduino_write(str(GUN.bulletcnt[gs][1])+"/"+str(GUN.bulletcnt[gs][0]))
        #print(ready)
        #print(ready[0])
        #print(ready)
        #510,505
        #ux=505
        #uy=511
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
    global bulletm,keys,F_on,R_on
    global bullet_item_stack,gun_item_stack
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
            asdf=0
            if GUN.gun_name[gs]=="AK47":asdf=0
            if GUN.left_bulletcnt[asdf]==0 and GUN.user_bulletcnt[hand]==0:print("Don't have bullet")
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
    #pygame.draw.circle(SURFACE,(251,206,177),(A.x,A.y),40)
    #A.img=pygame.transform.rotate(A.img,angle-A.mouse_angle)
    #A.angle=angle
    #print(angle,A.angle)
    A.mouse_angle_update()
def check(i,x,y):
    for g in range(i):
        posx=gun_item_stack[g].X
        posy=gun_item_stack[g].Y
        if math.sqrt(abs(posx-x)**2+abs(posy-y)**2)<75:return 0
    return 1
def check1(i,x,y):
    for g in range(i):
        posx=bullet_item_stack[g][0].X
        posy=bullet_item_stack[g][0].Y
        if math.sqrt(abs(posx-x)**2+abs(posy-y)**2)<75:return 0
    for g in range(rm):
        posx=gun_item_stack[g].X
        posy=gun_item_stack[g].Y
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
    cs=0
    no=0
    left=0
    right=0
    try:
        ser=serial.Serial('COM4',115200)
        #print("asd")
    except:
        no=1
    while 1:
        SURFACE.fill((0,0,0))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:break
        keyboard_img=pygame.image.load("keyboard.png")
        keyboard_img=pygame.transform.scale(keyboard_img,(320,160))
        cr_img=pygame.image.load("game_controller.png")
        cr_img=pygame.transform.scale(cr_img,(160,160))
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
bagsize=[[56,60],[69,60],[73,60],[79,60]]
asd=""
ser=0
before_start()
bulletm=[]
A=player()
zst=[]
for i in range(5):zst.append(zombie())
col=0
GUN=gun()
rm=random.randint(3,7)
gun_item_stack=[]
bullet_item_stack=[]
boost_item_stack=[]
#for i in range(5):boost_item_stack.append(boost_item(0))
crash_idx=-1
bt_crash_idx=-1
F_on=0
R_on=0
#print(asd)
for i in range(rm):
    while 1:
        X=random.randint(40,860)
        Y=random.randint(40,860)
        if check(i,X,Y)==1:
            gun_item_stack.append(gun_object(X,Y,0))
            break
rm1=random.randint(rm,rm+6)
for i in range(rm1):
    while 1:
        X=random.randint(40,860)
        Y=random.randint(40,860)
        if check1(i,X,Y)==1:
            bullet_item_stack.append([gun_object(X,Y,1),7.62,60])
            break
while 1:
    col+=1
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
    if asd=="keyboard":
        keyboard()
    if asd=="arduino":
        #print("CXVXCVXCV")
        arduino()
    z=0
    for i in range(len(bulletm)):
        bulletob=bulletm[i-z]
        bulletob.shot_move()
        er=0
        for g in range(len(zst)):
            if pygame.sprite.collide_mask(bulletob,zst[g-er]):
                zst[g-er].damage(2)
                if zst[g-er].life<=0:zst.pop(g);er+=1
                bulletm.pop(i-z);z+=1;break
        if bulletob.delete==1:bulletm.pop(i-z);z+=1
    #SURFACE.blit(A.img,(422,420))
    crash()
    for g in range(len(zst)):
        zst[g].watch_player()
        zst[g].bar_d()
    bullet_text()
    A.pld()
    pygame.display.update()
    if asd!="arduino":FPSCLOCK.tick(100)
    #else:FPSCLOCK.tick(1300)

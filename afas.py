# -*- coding: utf-8 -*-
#
#   rotation_ship_by_mouse.py
#   coding with python 3.5.3
#
#   http://codememo.tistory.com
#
 
import sys
import os
import math
import pygame
 
screen_width= 640
screen_height= 480
FPS= 60
 
class Background():# Background Image
    def __init__(self, screen):
        self.screen= screen
        self.background_image= pygame.image.load("player.png")
         
    def update(self):
        self.screen.blit(self.background_image, (0,0))
         
class Ship():# ship Image
    def __init__(self, screen, screen_width, screen_height):
        self.screen= screen
        self.screen_width= screen_width
        self.screen_height= screen_height
        self.ship_image= pygame.image.load("player.png")
        self.mouse_angle= 0
     
    def update(self):
        mouse_x= pygame.mouse.get_pos()[0]
        mouse_y= pygame.mouse.get_pos()[1]
         
        self.mouse_angle= math.pi- math.atan2(mouse_x- int(self.screen_width/ 2), mouse_y- int(self.screen_height/ 2))
        rotation_ship_image= pygame.transform.rotate(self.ship_image,-(int(math.degrees(self.mouse_angle)))+90)
         
        self.ship_image_pos= rotation_ship_image.get_rect()
        self.ship_image_pos.center= (int(screen_width/ 2),int(screen_height/ 2))
        self.screen.blit(rotation_ship_image,self.ship_image_pos)
         
def main():
    screen= pygame.display.set_mode([screen_width, screen_height],0,32)
    pygame.display.set_caption("Rotation ship by mouse")
 
    background= Background(screen)
    ship= Ship(screen, screen_width, screen_height)
    clock= pygame.time.Clock()
    running= True 
 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
                pygame.quit()
                sys.exit()
                 
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    running= False
         
        clock.tick(FPS)
        background.update()
        ship.update()
        pygame.display.flip()
         
if __name__== "__main__":
    main()

import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

#player class
class player(pygame.sprite.Sprite):
    #variables
    COLOR = (0,255,0)
    GRAVITY = 1
    ANIMATION_DELAY = 5

    def __init__(self,x,y,width,height,Sprites):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_speed = 0
        self.y_speed = 0
        self.sprites = Sprites
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_timer = 0
        self.jump_count = 0

    def jump(self):
        self.y_speed = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_timer = 0

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    def mv_left(self,speed):
        self.x_speed = -speed
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
  
    def mv_right(self,speed):
        self.x_speed = speed
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    #resets variables when hitting ground
    def landed(self):
        self.fall_timer = 0
        self.y_speed = 0
        self.jump_count = 0

    def bumped(self):
        self.count = 0
        self.y_speed += -1

    #updates velocities, and applies constant gravity
    def chr_loop(self,fps):
        self.y_speed += min(1,(self.fall_timer / fps) * self.GRAVITY)
        self.move(self.x_speed,self.y_speed)

        self.fall_timer +=1
        self.update_sprite()

#determines which sprite sheet to load
    def update_sprite(self):
        sprite_sheet = "idle"
        if  self.y_speed < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_speed > self.GRAVITY*2:
            sprite_sheet = "fall"
        elif self.x_speed != 0:
                sprite_sheet = "run"
                
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite =  sprites[sprite_index]
        self.animation_count +=1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self,window):
        window.blit(self.sprite,(self.rect.x,self.rect.y))



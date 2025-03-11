import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import collision_object
from collision_object import collision_object
#initalization environment blocks using collision object
class block(collision_object):
    def __init__(self,x,y,size,bload):
        super().__init__(x,y,size,size)
        block = bload
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)
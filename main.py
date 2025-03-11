import os
import random
import math
import pygame
import player
from os import listdir
from os.path import isfile, join
from player import player
import block
from block import block
#pygame platformer demo by Elijah Mendez, the Flyest Nerd you ever seen

pygame.init()

pygame.display.set_caption("Capstone Demo")

#game load variables
WIDTH = 1000
HEIGHT= 800
FPS = 60
PLAYER_SPEED = 5

window = pygame.display.set_mode((WIDTH,HEIGHT))

def flip(sprites):
        return [pygame.transform.flip(sprite,True,False) for sprite in sprites]


def load_sprites(dir1,dir2,width,height,direction = False):
            path = join("assets",dir1,dir2)
            images =[f for f in listdir(path) if isfile(join(path,f))]

            all_sprites = {}

            for image in images:
                sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()

                sprites = []
                for i in range(sprite_sheet.get_width() // width):
                    surface = pygame.Surface((width,height), pygame.SRCALPHA,32)
                    rect = pygame.Rect(i*width,0,width,height)
                    surface.blit(sprite_sheet, (0,0), rect)
                    sprites.append(pygame.transform.scale2x(surface))

                    if direction:
                        all_sprites[image.replace(".png","") + "_right"] =sprites
                        all_sprites[image.replace(".png","") + "_left"] = flip(sprites)
                    else:
                        all_sprites[image.replace(".png","")] = sprites

            return all_sprites


def load_block(size):
     path = join("assets","tiles","Terrain.png")
     image =pygame.image.load(path).convert_alpha()
     surface = pygame.Surface((size,size),pygame.SRCALPHA, 32 )
     rect = pygame.Rect(96,0,size,size)
     surface.blit(image,(0,0), rect)
     return pygame.transform.scale2x(surface)


def load_title():
    path = join("assets","background","Title.png")
    image = pygame.image.load(path).convert_alpha()
    return image



#loads background tiles into tile array
def get_background(name):
    image = pygame.image.load((join("assets","background", name)))
    _,_,width,height = image.get_rect()
    tiles = []
    for i in range (WIDTH // width + 1):
        for j in range(HEIGHT // height +1):
            pos = (i * width, j * height)
            tiles.append(pos)
    
    
    return tiles, image

#constantly redraws assets onto game window
def draw(window,background,bg_image,player,objects,caption):
    
    window.blit(caption,(500,500))
               
    for tile in background:
        window.blit(bg_image, tile)
    
    for obj in objects:
         obj.draw(window)
    
    window.blit(caption,(500,500))
    
    player.draw(window)

    pygame.display.update()

def vert_collide(player, objects, dy):
     collided_objects =[]
     for obj in objects:
          if pygame.sprite.collide_mask(player, obj):
               if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
               elif dy < 0:
                    player.rect.top = obj.rect.bottom
                    player.bumped()
          collided_objects.append(obj)
     return collided_objects



def map_movement(player, objects):
    key = pygame.key.get_pressed()
    player.x_speed = 0

    if key[pygame.K_LEFT]:
        player.mv_left(PLAYER_SPEED)
    if key[pygame.K_RIGHT]:
        player.mv_right(PLAYER_SPEED)
    
    vert_collide(player, objects, player.y_speed)



def main (window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Brown.png")
    run = True
    
    caption = load_title()
    sprites = load_sprites("characters","Eli_Jr",32,32,True)
    P1 = player(100,100,50,50,sprites)
    block_size = 96
    floor = [block(i*block_size,HEIGHT - block_size,block_size,load_block(block_size)) for i in range (-WIDTH//block_size, WIDTH *2 //block_size)]

    #event loop
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            
            #user quits game
            if event.type ==pygame.QUIT:
                run =False
                break
        
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_UP and P1.jump_count < 2:
                    P1.jump()

        P1.chr_loop(FPS)
        map_movement(P1,floor)
        draw(window,background, bg_image, P1, floor,caption)

    pygame.quit
    quit()

if __name__ == "__main__":
    main(window)
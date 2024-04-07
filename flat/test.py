import sys, os, math, random
import csv
import pygame
from pygame.locals import *
import button, image
import pytmx
from pytmx.util_pygame import load_pygame

pygame.init()

SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000

fps = 60
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision")

#create main rectangle & obstacle rectangle
obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)

#define colours
BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#hide mouse cursor
pygame.mouse.set_visible(False)

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Player:   
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 5


    def draw(self):
        keys = pygame.key.get_pressed()

        # Sauvegarde de la position précédente du joueur
        prev_x, prev_y = self.x, self.y

        if keys[pygame.K_q]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_z]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

        # Crée le rectangle du joueur
        self.rect = pygame.draw.rect(screen, BLUE, pygame.Rect(self.x, self.y, 100, 100))

        col = GREEN
        if self.rect.colliderect(layer1[0]):

            col = RED
            self.x, self.y = prev_x, prev_y
        
        pygame.draw.rect(screen, col, layer1[0])

        print(prev_x, prev_y, self.x, self.y)





tmx_data = load_pygame(os.path.join("assets", "map.tmx"))
map_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
    if hasattr(layer,'data'):
        for x,y,surf in layer.tiles():
            pos = (x * 128, y * 128)
            Tile(pos = pos, surf = surf, groups = map_group)
 
for obj in tmx_data.objects:
    pos = obj.x,obj.y
    if obj.type in ('Building', 'Vegetation'):
        Tile(pos = pos, surf = obj.image, groups = map_group)



layer1 = []


P1 = Player()



def tiled():
    map_group.draw(screen)


def l1g():

    # Convert visible_layers generator to a list
    visible_layers = list(tmx_data.visible_layers)

    # Check if layer_index is valid
    if 1 < 0 or 1 >= len(visible_layers):
        print("Invalid layer index")
        return

    layer = visible_layers[1]

    # Check if the layer has 'data' attribute
    if not hasattr(layer, 'data'):
        print("Layer does not contain tile data")
        return

    for surf in layer.tiles():
        
        surfrect = surf[2].get_rect(topleft=(surf[0]*128, surf[1]*128))

        layer1.append(surfrect)


l1g()

run = True
while run:
    #update background
    screen.fill(BG)     


    tiled()
    P1.draw()    
    #check collision and change colour

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()
    fpsClock.tick(fps)


pygame.quit()
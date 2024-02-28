import sys, os
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()


info = pygame.display.Info()
w = 600
h = 400


screen = pygame.display.set_mode((w, h))

pygame.display.set_caption("Murder")

murderU = pygame.image.load(os.path.join("assets", ""))


class Player():
    def __init__(self, x, y, sx, sy, nom, img, speed):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.nom = nom
        self.img = img
        self.speed = speed

    def draw(self):
        self.img = pygame.transform.scale(self.img, (self.sx, self.sy))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        screen.blit(self.img, (self.x, self.y))
  

def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False


M1 = Player(100, 100, 100, 100, "murder1", murderU, 5)

def draw():
    M1.draw()
  

# Game loop.
while True:
    screen.fill((0, 0, 0))
  
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f:
                if screen.get_flags() & FULLSCREEN:
                    pygame.display.set_mode((w, h))
                else:
                    pygame.display.set_mode((1920, 1080), FULLSCREEN)

  # Update.
  
  # Draw.
    draw()
  
    pygame.display.flip()
    fpsClock.tick(fps)
import sys, os, math
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()


info = pygame.display.Info()
w = 1000
h = 800


screen = pygame.display.set_mode((w, h))

pygame.display.set_caption("Murder")

knife = pygame.image.load(os.path.join("assets", "knife.png"))


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
        if keys[pygame.K_q]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_z]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

        pos = pygame.mouse.get_pos()

        x_dist = pos[0] - self.x
        y_dist = -(pos[1] - self.y)
        angle = math.degrees(math.atan2(y_dist, x_dist))

        knifeS = pygame.transform.rotate(self.img, angle - 90)
        knifeS_rect = knifeS.get_rect(center = (self.x, self.y))
        
        screen.blit(knifeS, knifeS_rect)
  

def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False

M1 = Player(100, 100, 100, 100, "Murder1", knife, 5)

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
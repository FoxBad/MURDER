import sys, os, math, random
import pygame
from pygame.locals import *
from network import Network

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()


info = pygame.display.Info()
w = 1000
h = 800


screen = pygame.display.set_mode((w, h))

pygame.display.set_caption("Murder")

clientNumber = 0


class Player():
    def __init__(self, x, y, sx, sy, speed):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.img = ino
        self.speed = speed

    def draw(self, win):
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
        
        win.blit(knifeS, knifeS_rect)
    


ino = pygame.image.load(os.path.join("assets", "ino.png"))
detect = pygame.image.load(os.path.join("assets", "detect.png"))
murder = pygame.image.load(os.path.join("assets", "murder.png"))

def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win,player, player2):
    screen.fill((0, 0, 0))
    player.draw(screen)
    player2.draw(screen)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0],startPos[1], 100, 100, 5)
    p2 = Player(0,0,100,100, 5)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f:
                if screen.get_flags() & FULLSCREEN:
                    pygame.display.set_mode((w, h))
                else:
                    pygame.display.set_mode((1920, 1080), FULLSCREEN)

        
        redrawWindow(screen, p, p2)

main()



import sys, os, math
import pygame
import socket, threading
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

info = pygame.display.Info()
w = 1000
h = 800

screen = pygame.display.set_mode((w, h))


class Player():
    def __init__(self, x, y, sx, sy, nom, img, speed):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.nom = nom
        self.img = img
        self.vie = 3
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
  
class Bullet:
    def __init__(self, tireur):
        self.tireur = tireur
        self.x = tireur.x
        self.y = tireur.y
        self.destx, self.desty = pygame.mouse.get_pos()
        self.rad = 5
        self.speed = 20  

        vect = (self.destx - self.x, self.desty - self.y)
        angle = math.atan2(vect[1], vect[0])
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed


    def draw(self):

        pygame.draw.circle(screen, BLACK, [self.x, self.y], self.rad, 0)


    def move(self):

        self.x += self.change_x
        self.y += self.change_y
                
        if self.x < 0 or self.x > info.current_w or self.y < 0 or self.y > info.current_h:
            bullets.remove(self)


def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False


BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


pygame.display.set_caption("Murder")

knife = pygame.image.load(os.path.join("assets", "knife.png"))

bullets = []

M1 = Player(100, 100, 100, 100, "Murder1", knife, 5)

def winsize():
    global ws, hs
    ws, hs = screen.get_size()

winsize()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Menu Principal", pygame.font.Font(None, 72), BLACK, screen, ws // 2, hs // 4)

        mx, my = pygame.mouse.get_pos()

        winsize()

        button_width = 400
        button_height = 100
        button_x = ws // 2 - button_width // 2
        button_y = hs // 2 - button_height // 2

        button_1 = pygame.Rect(button_x, button_y, button_width, button_height)
        button_2 = pygame.Rect(button_x, button_y + 200, button_width, button_height)

        pygame.draw.rect(screen, (0, 255, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        draw_text("Jouer", pygame.font.Font(None, 54), BLACK, screen, ws // 2, button_y + 50)
        draw_text("Quitter", pygame.font.Font(None, 54), BLACK, screen, ws // 2, button_y + 250)

        click = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if button_1.collidepoint((mx, my)):
                        game()
                    if button_2.collidepoint((mx, my)):
                        pygame.quit()
                        sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((w, h))
                    else:
                        pygame.display.set_mode((1920, 1080), FULLSCREEN)


        pygame.display.update()


def pause_menu():
    while True:
        draw_text("Pause", pygame.font.Font(None, 72), BLACK, screen, ws // 2, hs // 4)

        mx, my = pygame.mouse.get_pos()

        winsize()

        button_width = 400
        button_height = 100
        button_x = ws // 2 - button_width // 2
        button_y = hs // 2 - button_height // 2

        button_1 = pygame.Rect(button_x, button_y, button_width, button_height)
        button_2 = pygame.Rect(button_x, button_y + 200, button_width, button_height)

        pygame.draw.rect(screen, (0, 255, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        draw_text("Reprendre", pygame.font.Font(None, 54), BLACK, screen, ws // 2, button_y + 50)
        draw_text("Menu Principal", pygame.font.Font(None, 54), BLACK, screen, ws // 2, button_y + 250)

        click = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if button_1.collidepoint((mx, my)):
                        game()
                    if button_2.collidepoint((mx, my)):
                        main_menu()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((w, h))
                    else:
                        pygame.display.set_mode((1920, 1080), FULLSCREEN)
                if e.key == pygame.K_ESCAPE:
                    game()



        pygame.display.update()

def draw():
    M1.draw()
    for bullet in bullets:
        bullet.draw()

def bulletsmanage():
    for bullet in bullets:
        bullet.move()

def showall():
    draw()
    bulletsmanage()
    winsize()

# Game loop.
def game():
    running = True
    while running:
        screen.fill(WHITE)
    
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
                        """M1.x = M1.x*1920/w
                        M1.y = M1.x*1080/h
                        print(M1.x, M1.y)"""
                if e.key == pygame.K_SPACE:
                    new_bul = Bullet(M1)
                    bullets.append(new_bul)
                if e.key == pygame.K_ESCAPE:
                    pause_menu()


        showall()
    
        pygame.display.flip()
        fpsClock.tick(fps)

if __name__ == "__main__":
    main_menu()
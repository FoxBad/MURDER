
#-------------------------------IMPORT-----------------------------


import sys, os, math, random
import pygame
from pygame.locals import *
 

#-------------------------------INIT-----------------------------

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

info = pygame.display.Info()
w = 1000
h = 800

screen = pygame.display.set_mode((w, h))


#-------------------------------CLASS-----------------------------

class Player():
    def __init__(self, x, y, sx, sy, nom, speed, Ku, Kd, Kl, Kr):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.nom = nom      
        self.vie = 3
        self.speed = speed
        self.role = self.choisir_role()  # Choix aléatoire du rôle
        self.murder = False
        self.Ku = Ku
        self.Kd = Kd
        self.Kl = Kl
        self.Kr = Kr
        self.bulletlist = []

        
        if self.role == 'Innocent':
            self.img = ino
        if self.role == 'Murder':
            self.img = ino
        if self.role == 'Détective':
            self.img = detect


    def choisir_role(self):
        roles = ['Innocent', "Murder", 'Détective']
        poids_roles = [4, 1, 1]
        role = random.choices(roles, weights=poids_roles, k=1)[0]
        return role

    def draw(self):
        
        self.img = pygame.transform.scale(self.img, (self.sx, self.sy))
        keys = pygame.key.get_pressed()
        if keys[self.Kl]:
            self.x -= self.speed
        if keys[self.Kr]:
            self.x += self.speed
        if keys[self.Ku]:
            self.y -= self.speed 
        if keys[self.Kd]:
            self.y += self.speed

        pos = pygame.mouse.get_pos()

        x_dist = pos[0] - self.x
        y_dist = -(pos[1] - self.y)
        angle = math.degrees(math.atan2(y_dist, x_dist))

        image  = pygame.transform.rotate(self.img, angle)
        rect  = image.get_rect(center = (self.x, self.y))
        self.rect = pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)
        
        
        screen.blit(image, rect)



    

  
class Bullet:
    def __init__(self, tireur):
        self.tireur = tireur
        self.x = tireur.x
        self.y = tireur.y
        self.destx, self.desty = pygame.mouse.get_pos()
        self.radius = 5
        self.center = [self.x, self.y]
        self.speed = 20  
        


        vect = (self.destx - self.x, self.desty - self.y)
        angle = math.atan2(vect[1], vect[0])
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed


    def draw(self):


        self.circle = pygame.draw.circle(screen, BLACK, [self.x, self.y], self.radius, 0)
        self.rect = pygame.Rect(self.x-self.radius/2, self.y-self.radius/2, self.radius, self.radius)



    def move(self):

        self.x += self.change_x
        self.y += self.change_y
                


#-------------------------------VARIABLE-----------------------------

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

ino = pygame.image.load(os.path.join("assets", "ino.png"))
detect = pygame.image.load(os.path.join("assets", "detect.png"))
murder = pygame.image.load(os.path.join("assets", "murder.png"))
settings = pygame.image.load(os.path.join("assets", "settings.png"))
settings = pygame.transform.scale(settings, (75, 75))

bullets = []
players = []


M1 = Player(100, 100, 100, 100, "Murder1", 5,pygame.K_z,pygame.K_s,pygame.K_q,pygame.K_d)
M2 = Player(200, 300, 100, 100, "Murder2", 5, pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT )
players.append(M1)
players.append(M2)


#-------------------------------OTHER FUNCTION-----------------------------

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False

def winsize():
    global ws, hs
    ws, hs = screen.get_size()

winsize()


#-------------------------------MAIN MENU-----------------------------

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

#-------------------------------PAUSE MENU-----------------------------


def pause_menu():
    while True:
        screen.fill(WHITE)
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

        set_rect = settings.get_rect(center=(50, 50))
        screen.blit(settings, set_rect)

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
                    if set_rect.collidepoint((mx, my)):
                        set_menu()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((w, h))
                    else:
                        pygame.display.set_mode((1920, 1080), FULLSCREEN)
                if e.key == pygame.K_ESCAPE:
                    game()



        pygame.display.update()


#-------------------------------OPTIONS MENU-----------------------------


def set_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Options", pygame.font.Font(None, 72), BLACK, screen, ws // 2, (hs // 4) -100)

        mx, my = pygame.mouse.get_pos()

        winsize()

        button_width = 400
        button_height = 100
        button_x = ws // 2 - button_width // 2
        button_y = hs // 2 - button_height // 2

        button_1 = pygame.Rect(button_x, button_y -150, button_width, button_height)
        button_2 = pygame.Rect(button_x , button_y, button_width, button_height)
        button_3 = pygame.Rect(button_x, button_y + 150, button_width, button_height)
        button_4 = pygame.Rect(button_x, button_y + 300, button_width, button_height)

        pygame.draw.rect(screen, (100, 100, 100), button_1)
        pygame.draw.rect(screen, (100, 100, 100), button_2)
        pygame.draw.rect(screen, (100, 100, 100), button_3)
        pygame.draw.rect(screen, (255, 0, 0), button_4)

        draw_text("Murder", pygame.font.Font(None, 54), BLACK, screen, button_x+200, button_y - 100)
        draw_text("Innocent", pygame.font.Font(None, 54), BLACK, screen, button_x+200, button_y+50)
        draw_text("Détective", pygame.font.Font(None, 54), BLACK, screen, button_x+200, button_y + 200)
        draw_text("Retour", pygame.font.Font(None, 54), BLACK, screen, button_x+200, button_y + 350)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:

                    for player in players:

                        if button_1.collidepoint((mx, my)):
                            player.role = "Murder"
                        if button_2.collidepoint((mx, my)):
                            player.role = 'Innocent'
                        if button_3.collidepoint((mx, my)):
                            player.role = "Détective"
                        if button_4.collidepoint((mx, my)):
                            pause_menu()
                    

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((w, h))
                    else:
                        pygame.display.set_mode((1920, 1080), FULLSCREEN)
                if e.key == pygame.K_ESCAPE:
                    pause_menu()

        pygame.display.update()



#-------------------------------JEU-----------------------------


def playermanage():
        

    draw_text(M1.role, pygame.font.Font(None, 54), BLACK, screen, ws*18 // 20, hs // 20)
    draw_text(M2.role, pygame.font.Font(None, 54), BLACK, screen, ws*10 // 20, hs // 20)


    
    for player in players:

        player.draw()

        if player.murder == True and player.role == "Murder":
            pygame.draw.ellipse(screen, BLACK, [player.x-player.sx, player.y-player.sy, 200, 200], 5)

        if player.role == 'Innocent':
            player.murder == False
            player.img = ino
        if player.role == 'Détective':
            player.murder == False
            player.img = detect




def bulletsmanage():
    for player in players:

        for bullet in player.bulletlist:
            bullet.draw()
            bullet.move() 

            otherplayer = players.copy()
            otherplayer.remove(player)
            
            for player2 in otherplayer:
                if bullet.rect.colliderect(player2.rect):
                    player.bulletlist.remove(bullet)

            if bullet.x < 0 or bullet.x > info.current_w or bullet.y < 0 or bullet.y > info.current_h:
                player.bulletlist.remove(bullet)




  
    


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

                if e.key == pygame.K_ESCAPE:
                    pause_menu()




                for player in players:
                    
                    if e.key == pygame.K_SPACE and player.role == 'Détective':
                        new_bul = Bullet(player)
                        player.bulletlist.append(new_bul)

                    if e.key == pygame.K_SPACE and player.role == "Murder" and player.murder == True:
                        pygame.draw.circle(screen, RED, [player.x, player.y], 99, 0)

                    if e.key == pygame.K_e and player.role == "Murder":
                        player.img = murder
                        player.murder = True
                    if e.key == pygame.K_r and player.role == "Murder":
                        player.img = ino
                        player.murder = False
                    



        playermanage()
        bulletsmanage()
        winsize()
    
        pygame.display.flip()
        fpsClock.tick(fps)


#-------------------------------START-----------------------------

if __name__ == "__main__":
    main_menu()

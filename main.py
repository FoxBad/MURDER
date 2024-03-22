
#-------------------------------IMPORT-----------------------------


import sys, os, math, random
import csv
import pygame
from pygame.locals import *
import button, image
import pytmx

#-------------------------------INIT-----------------------------

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

info = pygame.display.Info()
w = 1000
h = 800

pygame.display.set_caption("APEO - BETA")
icon = pygame.image.load(os.path.join("assets", "logot.png"))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((w, h))



def winsize():
    global ws, hs
    ws, hs = screen.get_size()

winsize()


#-------------------------------CLASS-----------------------------

class Player():
    def __init__(self, x, y, sx, sy, nom, speed, Ku, Kd, Kl, Kr):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.nom = nom      
        self.vie = 1
        self.etat = True
        self.speed = speed
        self.role = self.choisir_role()  # Choix aléatoire du rôle
        self.murderstat = False
        self.Ku = Ku
        self.Kd = Kd
        self.Kl = Kl
        self.Kr = Kr
        self.bulletlist = []
        self.bullet = 3
        self.destx, self.desty = pygame.mouse.get_pos()
        self.sector = sector
        
        
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

    def update(self):
        
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
        
    def orientation(self):

        pos = pygame.mouse.get_pos()

        x_dist = pos[0] - self.x
        y_dist = -(pos[1] - self.y)
        
        angle = math.degrees(math.atan2(y_dist, x_dist))
    
        image  = pygame.transform.rotate(self.img, angle)
        rect  = image.get_rect(center = (self.x, self.y))
        self.rect = pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)

        screen.blit(image, rect)
    
    def murder(self):


        """
        if self.murderstat == True and self.role == "Murder":
            
            pos = pygame.mouse.get_pos()

            x_dist = pos[0] - self.x
            y_dist = -(pos[1] - self.y)
        
            angle = math.degrees(math.atan2(y_dist, x_dist))
    
            image  = pygame.transform.rotate(self.sector, angle)
            rect = image.get_rect(center=(self.x - math.sin(math.radians(angle)), self.y - math.cos(math.radians(angle))))

            screen.blit(image, rect)
            """         

    def innocent(self):
        if self.role == 'Innocent':
            self.murder == False
            self.img = ino

    def detective(self):
        if self.role == 'Détective':
            self.murder == False
            self.img = detect

    def perdre_vie(self):
        self.vie -= 1

        if self.vie <=0:
            self.etat = False

    

  
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


button_width = 375
button_height = 150

text_width = 500
text_height = 200


ino = pygame.image.load(os.path.join("assets", "ino.png"))

detect = pygame.image.load(os.path.join("assets", "detect.png"))

murder = pygame.image.load(os.path.join("assets", "murder.png"))

sector = pygame.image.load(os.path.join("assets", "sector.png"))
sector = pygame.transform.scale(sector, (100, 100))
sector  = pygame.transform.rotate(sector, 300)


players = []

M1 = Player(ws*5 // 20, hs*4 // 20, 100, 100, "Murder1", 5,pygame.K_z,pygame.K_s,pygame.K_q,pygame.K_d)
M2 = Player(ws*15 // 20, hs*4 // 20, 100, 100, "Murder2", 5, pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT )
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

def tryquit():
    pygame.quit()
    sys.exit()



#-------------------------------MAIN MENU-----------------------------

def main_menu():
    while True:

        mx, my = pygame.mouse.get_pos()

        winsize()

        button_x = ws // 2
        button_y = hs // 2

        fond = image.Image(ws // 2, hs // 2, "fond.png", (ws,hs))
        fond.draw(screen)
        
        play_button = button.Button(button_x, button_y +50, "play.png", (button_width,button_height))
        if play_button.draw(screen):
            game()

        quit_button = button.Button(button_x, button_y +250, "quit.png", (button_width,button_height))
        if quit_button.draw(screen):
            tryquit()

        settings_button = button.Button(50, 50, "settings.png", (75, 75))
        if settings_button.draw(screen):
            set_menu()

        logo = image.Image(ws // 2, hs // 5, "logo.png", (300,300))
        logo.draw(screen)
        

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
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

        fondp = image.Image(ws // 2, hs // 2, "fondp.jpg", (ws,hs))
        fondp.draw(screen)

        pause = image.Image(ws // 2, hs // 4, "pause.png", (text_width,text_height))
        pause.draw(screen)

        mx, my = pygame.mouse.get_pos()

        winsize()

        button_x = ws // 2
        button_y = hs // 2

        resume_button = button.Button(button_x, button_y +50, "resume.png", (button_width,button_height))
        if resume_button.draw(screen):
            game()

        menu_button = button.Button(button_x, button_y +250, "menu.png", (button_width,button_height))
        if menu_button.draw(screen):
            main_menu()

        settings_button = button.Button(50, 50, "settings.png", (75, 75))
        if settings_button.draw(screen):
            set_jeu()


        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    game()


        pygame.display.update()


#-------------------------------OPTIONS JEU-----------------------------


def set_jeu():
    while True:

        mx, my = pygame.mouse.get_pos()

        winsize()

        button_width = 250
        button_height = 100
        
        button_x = ws // 2
        button_y = hs // 2

        setfond = image.Image(ws // 2, hs // 2, "setfond.png", (ws,hs))
        setfond.draw(screen)
        
        settingst = image.Image(ws // 2, hs // 7, "settingst.png", (text_width,text_height))
        settingst.draw(screen)

        button_1 = button.Button(button_x -250, button_y -150, "murderb.png", (button_width,button_height))
        if button_1.draw(screen):
            M1.role = "Murder"

        button_2 = button.Button(button_x -250, button_y, "innocentb.png", (button_width,button_height))
        if button_2.draw(screen):
            M1.role = "Innocent"

        button_3 = button.Button(button_x -250, button_y + 150, "detectiveb.png", (button_width,button_height))
        if button_3.draw(screen):
            M1.role = "Détective"

        button_4 = button.Button(button_x +250, button_y -150, "add.png", (button_width,button_height))
        if button_4.draw(screen):
            pass

        button_5 = button.Button(button_x +250, button_y, "add.png", (button_width,button_height))
        if button_5.draw(screen):
            pass

        button_6 = button.Button(button_x +250, button_y + 150, "add.png", (button_width,button_height))
        if button_6.draw(screen):
            pass

        return_button = button.Button(button_x, button_y +300, "return.png", (button_width,button_height))
        if return_button.draw(screen):
            pause_menu()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pause_menu()

        pygame.display.update()

#-------------------------------OPTIONS MENU-----------------------------


def set_menu():
    while True:

        winsize()

        button_width = 250
        button_height = 100
        
        button_x = ws // 2
        button_y = hs // 2

        setfond = image.Image(ws // 2, hs // 2, "setfond.png", (ws,hs))
        setfond.draw(screen)
        
        settingst = image.Image(ws // 2, hs // 7, "settingst.png", (text_width,text_height))
        settingst.draw(screen)

        button_1 = button.Button(button_x -250, button_y -150, "add.png", (button_width,button_height))
        if button_1.draw(screen):
            pass

        button_2 = button.Button(button_x -250, button_y, "add.png", (button_width,button_height))
        if button_2.draw(screen):
            pass

        button_3 = button.Button(button_x -250, button_y + 150, "add.png", (button_width,button_height))
        if button_3.draw(screen):
            pass

        button_4 = button.Button(button_x +250, button_y -150, "add.png", (button_width,button_height))
        if button_4.draw(screen):
            pass

        button_5 = button.Button(button_x +250, button_y, "add.png", (button_width,button_height))
        if button_5.draw(screen):
            pass

        button_6 = button.Button(button_x +250, button_y + 150, "add.png", (button_width,button_height))
        if button_6.draw(screen):
            pass

        return_button = button.Button(button_x, button_y + 300, "return.png", (button_width,button_height))
        if return_button.draw(screen):
            main_menu()
            
        

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((w, h))
                    else:
                        pygame.display.set_mode((1920, 1080), FULLSCREEN)
                if e.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()

#-------------------------------JEU-----------------------------

def checkalive():
    for player in players:
        if player.etat == False:
        
            players.remove(player)


def playermanage():
    

    for player in players:
        draw_text(player.role, pygame.font.Font(None, 30), BLACK, screen, player.x, player.y-80)
        
        if player.role == 'Détective':
            draw_text(str(player.bullet) + " •", pygame.font.Font(None, 30), BLACK, screen, player.x, player.y-60)


        #draw_text(player.role, pygame.font.Font(None, 54), BLACK, screen, ws*15 // 20, hs // 20)
        #draw_text(str(player.bullet) + " •", pygame.font.Font(None, 54), BLACK, screen, ws*15 // 20, hs*2 // 20)

    for player in players:

        player.update()
        player.orientation()
        player.murder()
        player.innocent()
        player.detective()
            

def checkcollision(p1, c1):

    otherplayer = players.copy()
    otherplayer.remove(p1)
    for player in otherplayer:
        # Calculer la distance entre le centre du cercle et le bord le plus proche du rectangle
        distance_x = abs(c1.centerx - player.rect.centerx) - player.rect.width / 2
        distance_y = abs(c1.centery - player.rect.centery) - player.rect.height / 2

        # Déterminer s'il y a collision
        if distance_x ** 2 + distance_y ** 2 <= 100 ** 2:
            player.perdre_vie()


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
                    player2.perdre_vie()

            if bullet.x < 0 or bullet.x > info.current_w or bullet.y < 0 or bullet.y > info.current_h:
                player.bulletlist.remove(bullet)



def event():
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:
                pause_menu()


            for player in players:
                if e.key == pygame.K_SPACE and player.role == 'Détective' and player.bullet > 0:
                    new_bul = Bullet(player)
                    player.bullet -= 1
                    player.bulletlist.append(new_bul)

                #if e.key == pygame.K_SPACE and player.role == "Murder" and player.murderstat == True:
                    #circle = pygame.draw.circle(screen, RED, [player.x, player.y], 100, 0)
                    #checkcollision(player, circle)


                if e.key == pygame.K_e and player.role == "Murder":
                    player.img = murder
                    player.murderstat = True
                    
                if e.key == pygame.K_r and player.role == "Murder":
                    player.img = ino
                    player.murderstat = False


# Game loop.
def game():
    running = True
    while running:
        screen.fill(WHITE)

        
        event()
        checkalive()
        playermanage()
        bulletsmanage()
        winsize()
    
        pygame.display.flip()
        fpsClock.tick(fps)


#-------------------------------START-----------------------------

if __name__ == "__main__":
    main_menu()

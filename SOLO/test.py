
#-------------------------------IMPORT-----------------------------


import sys, os, math, random
import csv
import pygame
from pygame.locals import *
import button, image
import pytmx
from pytmx.util_pygame import load_pygame
from pygame import Vector2


#-------------------------------INIT-----------------------------
pygame.init()

fps = 120
fpsClock = pygame.time.Clock()

info = pygame.display.Info()
w = 1000
h = 800

pygame.display.set_caption("APEO - BETA")
icon = pygame.image.load(os.path.join("assets", "logo2.png"))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((w, h))

def winsize():
    global ws, hs
    ws, hs = screen.get_size()

winsize()


#-------------------------------CLASS-----------------------------


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sx, sy, vel, Ku, Kd, Kl, Kr, groups):
        super().__init__(groups)
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy 
        self.size = (sx, sy)
        self.vie = 1
        self.etat = True
        self.vel = vel
        self.role = self.choisir_role()  # Choix aléatoire du rôle
        self.Assassinstat = False
        self.Magestat = False
        self.Ku = Ku
        self.Kd = Kd
        self.Kl = Kl
        self.Kr = Kr
        self.bulletlist = []
        self.bullet = 3
        self.base_img = paysan



    def choisir_role(self):
        roles = ['Paysan', "Assassin", 'Mage']
        poids_roles = [10, 1, 1]
        role = random.choices(roles, weights=poids_roles, k=1)[0]
        return role

    def update(self):

        self.image = pygame.transform.scale(self.base_img, (self.sx, self.sy))

        keys = pygame.key.get_pressed()

        prev_x, prev_y = self.x, self.y
                
        
        if keys[self.Kl]:
            self.x -= self.vel
        if keys[self.Kr]:
            self.x += self.vel
        if keys[self.Ku]:
            self.y -= self.vel 
        if keys[self.Kd]:
            self.y += self.vel


        velx, vely = self.x - prev_x, self.y - prev_y

            
        self.rect = pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)
        #self.rect = pygame.draw.rect(screen, BLACK, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)
        

        for sprite in layer2_group:
            if pygame.sprite.collide_rect(sprite, self):
                self.x, self.y = prev_x, prev_y
        """
        
            if vely > 0:
                self.temprect = self.rect
                self.temprect.y += self.vel

                if sprite.rect.colliderect(self.temprect):
                    self.vel = sprite.rect.top - self.rect.bottom

                else:
                    self.vel = 2

        """

    def orientation(self):

        pos = pygame.mouse.get_pos()
        self.x_dist = pos[0] - self.x
        self.y_dist = -(pos[1] - self.y)
        self.angle = math.degrees(math.atan2(self.y_dist, self.x_dist))
        self.image  = pygame.transform.rotate(self.image, self.angle)
        self.rectangle  = self.image.get_rect(center = (self.x, self.y))

        self.mask = pygame.mask.from_surface(self.image)
        self.pos = (self.x,self.y)

        screen.blit(self.image, self.rectangle)


    def Assassin(self):
        if self.role == 'Assassin' and self.Assassinstat == True:
            self.vect = pygame.Vector2((self.x, self.y))
            self.sector = Sector(self.vect)
            self.sector.update()

    def Paysan(self):
        if self.role == 'Paysan':
            self.Assassinstat == False
            self.Magestat == False

    def mage(self):
        if self.role == 'Mage':
            self.Assassinstat == False

    def perdre_vie(self):
        self.vie -= 1
        if self.vie <=0:
            self.etat = False
        
    def checkalive(self):
        if self.etat == False:
            RedCross(self.pos, deathgroup)
            self.kill()



class RedCross(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos = pos
        self.image = redcross
        self.rect = self.image.get_rect(center = self.pos)
    
    def draw(self):
        screen.blit(self.image, self.rect)



class Sector(pygame.sprite.Sprite):
    def __init__(self, pivot):
        self.pivot = pivot
        self.pos = pivot + (70, 0)
        self.image_orig = sector
        self.image = self.image_orig
        self.rect = self.image.get_rect(center = self.pos)
        
    def update(self):
        
        mouse_pos = Vector2(pygame.mouse.get_pos())
        
        mouse_offset = mouse_pos - self.pivot
        mouse_angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))
        
        self.image, self.rect = rotate_on_pivot(self.image_orig, mouse_angle, self.pivot, self.pos)

        self.mask = pygame.mask.from_surface(self.image)
    
        screen.blit(self.image, self.rect)


class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = pygame.Rect(0, 0, 4400, 4400)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - ws // 2 
        self.offset.y = player.rect.centery - hs // 2 

        floor_offset_pos = self.floor_rect.topleft - self.offset

        for tiles in layer1_group:
            screen.blit(tiles.draw(screen), floor_offset_pos)

        for sprite in players_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

  
class Bullet(pygame.sprite.Sprite):
    def __init__(self, tireur):
        self.tireur = tireur
        self.x = tireur.x
        self.y = tireur.y
        self.image = fireball
        self.destx, self.desty = pygame.mouse.get_pos()
        self.speed = 20  
        
        vect = (self.destx - self.x, self.desty - self.y)
        angle = math.atan2(vect[1], vect[0])
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed


    def draw(self):

        self.rect = self.image.get_rect(center=(self.x,self.y))        
        screen.blit(self.image, self.rect)

    def move(self):

        self.x += self.change_x
        self.y += self.change_y
                


#-------------------------------TILED-----------------------------

tmx_data = load_pygame(os.path.join("assets", "map.tmx"))
layer1_group = pygame.sprite.Group()  # Groupe pour la première couche
layer2_group = pygame.sprite.Group()  # Groupe pour la deuxième couche

for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 128, y * 128)
            if layer.name == '1':  # Si c'est la première couche
                Tile(pos=pos, surf=surf, groups=layer1_group)
            elif layer.name == '2':  # Si c'est la deuxième couche
                Tile(pos=pos, surf=surf, groups=layer2_group)

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


paysan = pygame.image.load(os.path.join("assets", "paysan.png"))
paysan  = pygame.transform.rotate(paysan, 90)

mage = pygame.image.load(os.path.join("assets", "mage.png"))
mage  = pygame.transform.rotate(mage, 90)

assassin = pygame.image.load(os.path.join("assets", "assassin.png"))
assassin  = pygame.transform.rotate(assassin, 90)

redcross = pygame.image.load(os.path.join("assets", "redcross.png"))
redcross = pygame.transform.scale(redcross, (60, 60))

fireball = pygame.image.load(os.path.join("assets", "fireball.png"))
fireball = pygame.transform.scale(fireball, (20, 20))

sector = pygame.image.load(os.path.join("assets", "sectore3.png"))
sector = pygame.transform.scale(sector, (200, 200))
sector  = pygame.transform.rotate(sector, 275)

players_group = pygame.sprite.Group()
deathgroup = pygame.sprite.Group()

M1 = Player(ws*5 // 20, hs*4 // 20, 100, 100, 4,pygame.K_z,pygame.K_s,pygame.K_q,pygame.K_d, players_group)
M2 = Player(ws*15 // 20, hs*4 // 20, 100, 100, 4, pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT, players_group)

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

def rotate_on_pivot(image, angle, pivot, origin):
    
    surf = pygame.transform.rotate(image, angle)
    
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = surf.get_rect(center = offset)
    
    return surf, rect





#-------------------------------MAIN MENU-----------------------------

def main_menu():
    while True:

        pos = pygame.mouse.get_pos()

        winsize()

        button_x = ws // 2
        button_y = hs // 2

        fond = image.Image(ws // 2, hs // 2, "fond.png", (ws,hs), screen)
        
        play_button = button.Button(button_x, button_y +50, "play.png", (button_width,button_height), screen)

        quit_button = button.Button(button_x, button_y +250, "quit.png", (button_width,button_height), screen)

        settings_button = button.Button(50, 50, "settings.png", (75, 75), screen)

        logo = image.Image(ws // 2, hs // 5, "logo22.png", (300,300), screen)
        

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(pos):
                    game()
                if quit_button.rect.collidepoint(pos):
                    tryquit()
                if settings_button.rect.collidepoint(pos):
                    set_menu()


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
        pos = pygame.mouse.get_pos()


        fondp = image.Image(ws // 2, hs // 2, "fondp.jpg", (ws,hs), screen)

        pause = image.Image(ws // 2, hs // 4, "pause.png", (text_width,text_height), screen)

        winsize()

        button_x = ws // 2
        button_y = hs // 2

        resume_button = button.Button(button_x, button_y +50, "resume.png", (button_width,button_height), screen)

        menu_button = button.Button(button_x, button_y +250, "menu.png", (button_width,button_height), screen)

        settings_button = button.Button(50, 50, "settings.png", (75, 75), screen)



        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.rect.collidepoint(pos):
                    game()
                if menu_button.rect.collidepoint(pos):
                    main_menu()
                if settings_button.rect.collidepoint(pos):
                    set_jeu()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    game()


        pygame.display.update()


#-------------------------------OPTIONS JEU-----------------------------


def set_jeu():
    while True:

        pos = pygame.mouse.get_pos()

        winsize()

        button_width = 250
        button_height = 100
        
        button_x = ws // 2
        button_y = hs // 2

        setfond = image.Image(ws // 2, hs // 2, "setfond.png", (ws,hs), screen)
        settingst = image.Image(ws // 2, hs // 7, "settingst.png", (text_width,text_height), screen)

        button_1 = button.Button(button_x -250, button_y -150, "murderb.png", (button_width,button_height), screen)
        button_2 = button.Button(button_x -250, button_y, "innocentb.png", (button_width,button_height), screen)
        button_3 = button.Button(button_x -250, button_y + 150, "detectiveb.png", (button_width,button_height), screen)
        button_4 = button.Button(button_x +250, button_y -150, "add.png", (button_width,button_height), screen)
        button_5 = button.Button(button_x +250, button_y, "add.png", (button_width,button_height), screen)
        button_6 = button.Button(button_x +250, button_y + 150, "add.png", (button_width,button_height), screen)
        return_button = button.Button(button_x, button_y +300, "return.png", (button_width,button_height), screen)
            

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if button_1.rect.collidepoint(pos):
                    M1.role = "Assassin"
                if button_2.rect.collidepoint(pos):
                    M1.role = "Paysan"
                if button_3.rect.collidepoint(pos):
                    M1.role = "Mage"

                if return_button.rect.collidepoint(pos):
                    pause_menu()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pause_menu()

        pygame.display.update()

#-------------------------------OPTIONS MENU-----------------------------


def set_menu():
    while True:

        pos = pygame.mouse.get_pos()

        winsize()

        button_width = 250
        button_height = 100
        
        button_x = ws // 2
        button_y = hs // 2

        setfond = image.Image(ws // 2, hs // 2, "setfond.png", (ws,hs), screen)
        settingst = image.Image(ws // 2, hs // 7, "settingst.png", (text_width,text_height), screen)

        button_1 = button.Button(button_x -250, button_y -150, "add.png", (button_width,button_height), screen)
        button_2 = button.Button(button_x -250, button_y, "add.png", (button_width,button_height), screen)
        button_3 = button.Button(button_x -250, button_y + 150, "add.png", (button_width,button_height), screen)
        button_4 = button.Button(button_x +250, button_y -150, "add.png", (button_width,button_height), screen)
        button_5 = button.Button(button_x +250, button_y, "add.png", (button_width,button_height), screen)
        button_6 = button.Button(button_x +250, button_y + 150, "add.png", (button_width,button_height), screen)
        return_button = button.Button(button_x, button_y +300, "return.png", (button_width,button_height), screen)
            
        

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   

            if e.type == pygame.MOUSEBUTTONDOWN:
                if return_button.rect.collidepoint(pos):
                    main_menu()

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


def tiled():
    layer1_group.draw(screen)
    layer2_group.draw(screen)


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



def playermanage():

    for player in players_group:
        player.Assassin() 
        player.Paysan()
        player.mage()
        player.update()
        player.orientation()
        player.checkalive()

    for player in players_group:
        draw_text(player.role, pygame.font.Font(None, 30), BLACK, screen, player.x, player.y-80)

        #draw_text(str(player.vie), pygame.font.Font(None, 30), BLACK, screen, player.x, player.y-60)
        
        if player.role == 'Mage':
            draw_text(str(player.bullet) + " •", pygame.font.Font(None, 30), BLACK, screen, player.x, player.y-60)
            

def death():
    deathgroup.draw(screen)


def bulletsmanage():
    for player in players_group:
        for bullet in player.bulletlist:


            bullet.draw()
            bullet.move() 

            otherplayer = players_group.copy()
            otherplayer.remove(player)

            
            for player2 in otherplayer:
                if pygame.sprite.collide_mask(bullet, player2):
                    player2.perdre_vie()
                    player.bulletlist.remove(bullet)

            if bullet.x < 0 or bullet.x > info.current_w or bullet.y < 0 or bullet.y > info.current_h:
                player.bulletlist.remove(bullet)

            for sprite in layer2_group:
                if pygame.sprite.collide_mask(bullet, sprite):
                    player.bulletlist.remove(bullet)



def event():
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
            
        
        for player in players_group:

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_ESCAPE:
                    pause_menu()

                if e.key == pygame.K_e and player.role == "Assassin":
                    player.base_img = assassin
                    player.Assassinstat = True
                    
                if e.key == pygame.K_r and player.role == "Assassin":
                    player.base_img = paysan
                    player.Assassinstat = False
                

                if e.key == pygame.K_e and player.role == "Mage":
                    player.base_img = mage
                    player.Magestat = True
                    
                if e.key == pygame.K_r and player.role == "Mage":
                    player.base_img = paysan
                    player.Magestat = False
                    


            if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and player.role == 'Mage' and player.Magestat == True and player.bullet > 0:
                new_bul = Bullet(player)
                player.bullet -= 1
                player.bulletlist.append(new_bul)

            if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and player.role == "Assassin" and player.Assassinstat == True:

                otherplayer = players_group.copy()
                otherplayer.remove(player)
                
                for player2 in otherplayer:
                    if pygame.sprite.collide_mask(player.sector, player2):
                        player2.perdre_vie()
                    


# Game loop.
def game():
    running = True
    while running:
        screen.fill(WHITE)
        
        tiled()
        death()
        playermanage()
        bulletsmanage()
        winsize()

        event()
        pygame.display.flip()
        fpsClock.tick(fps)


#-------------------------------START-----------------------------

if __name__ == "__main__":
    main_menu()

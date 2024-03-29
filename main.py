
#-------------------------------IMPORT-----------------------------


import sys, os, math, random
import csv
import pygame
from pygame.locals import *
import button, image
import pytmx
from pytmx.util_pygame import load_pygame


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


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sx, sy, nom, speed, Ku, Kd, Kl, Kr, groups):
        super().__init__(groups)
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


        self.rect = self.img.get_rect(center = (self.x,self.y))


    def choisir_role(self):
        roles = ['Innocent', "Murder", 'Détective']
        poids_roles = [4, 1, 1]
        role = random.choices(roles, weights=poids_roles, k=1)[0]
        return role

    def update(self):

        self.img = pygame.transform.scale(self.img, (self.sx, self.sy))

        
        self.x2, self.y2 = self.x, self.y

        keys = pygame.key.get_pressed()
        if keys[self.Kl]:
            self.x -= self.speed
        if keys[self.Kr]:
            self.x += self.speed
        if keys[self.Ku]:
            self.y -= self.speed 
        if keys[self.Kd]:
            self.y += self.speed


        self.dx, self.dy = self.x-self.x2, self.y-self.y2

        print(self.dx, self.dy)
        for player in players_group:
            for surf in layer1:
                if checkcollision(player, layer1):
                    if self.dx > 0:
                        # Le joueur se déplace vers la droite                    
                        player.rect.right = surf.rect.left  # Ajuste la position du joueur à gauche du tile
                    else:
                        # Le joueur se déplace vers la gauche
                        player.rect.left = surf.rect.right  # Ajuste la position du joueur à droite du tile
                    # Si le joueur se déplace verticalement (vers le haut ou le bas)

                    if self.dy > 0:

                        # Le joueur se déplace vers le bas
                        player.rect.bottom = surf.rect.top  # Ajuste la position du joueur au-dessus du tile
                        
                    else:
                        # Le joueur se déplace vers le haut
                        player.rect.top = surf.rect.bottom
                    

    def orientation(self):

        pos = pygame.mouse.get_pos()

        x_dist = pos[0] - self.x
        y_dist = -(pos[1] - self.y)
        
        angle = math.degrees(math.atan2(y_dist, x_dist))
    
        image  = pygame.transform.rotate(self.img, angle)
        self.rect2  = image.get_rect(center = (self.x, self.y))
        self.rect = pygame.draw.rect(screen, BLACK, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy))
        #self.rect = pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)

        screen.blit(image, self.rect2)
    
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


class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = pygame.Rect(0, 0, 4400, 4400)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - ws // 2 
        self.offset.y = player.rect.centery - hs // 2 

        floor_offset_pos = self.floor_rect.topleft - self.offset

        for tiles in map_group:
            screen.blit(tiles.draw(screen), floor_offset_pos)

        for sprite in players_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

  
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
                


#-------------------------------TILED-----------------------------

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
inogold = pygame.image.load(os.path.join("assets", "inogold.png"))

detect = pygame.image.load(os.path.join("assets", "detect.png"))
murder = pygame.image.load(os.path.join("assets", "murder.png"))

sector = pygame.image.load(os.path.join("assets", "sector.png"))
sector = pygame.transform.scale(sector, (100, 100))
sector  = pygame.transform.rotate(sector, 300)

players_group = pygame.sprite.Group()
layer1 = pygame.sprite.Group()


M1 = Player(ws*5 // 20, hs*4 // 20, 100, 100, "Murder1", 5,pygame.K_z,pygame.K_s,pygame.K_q,pygame.K_d, players_group)
#M2 = Player(ws*15 // 20, hs*4 // 20, 100, 100, "Murder2", 5, pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT, players_group)

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

        pos = pygame.mouse.get_pos()

        winsize()

        button_x = ws // 2
        button_y = hs // 2

        fond = image.Image(ws // 2, hs // 2, "fond.png", (ws,hs), screen)
        
        play_button = button.Button(button_x, button_y +50, "play.png", (button_width,button_height), screen)

        quit_button = button.Button(button_x, button_y +250, "quit.png", (button_width,button_height), screen)

        settings_button = button.Button(50, 50, "settings.png", (75, 75), screen)

        logo = image.Image(ws // 2, hs // 5, "logo.png", (300,300), screen)
        

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
                    M1.role = "Murder"
                if button_2.rect.collidepoint(pos):
                    M1.role = "Innocent"
                if button_3.rect.collidepoint(pos):
                    M1.role = "Détective"

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
        print(surf[2])
        layer1.add(surf[2])


def checkcollision(element, group):
    for surf in group:
        collide = pygame.Rect.colliderect(element.rect, surf[2].rect)
        if collide:
            return True


"""
def checkcollision2(p1, c1):

    otherplayer = players_group.copy()
    otherplayer.remove(p1)
    for player in otherplayer:
        # Calculer la distance entre le centre du cercle et le bord le plus proche du rectangle
        distance_x = abs(c1.centerx - player.rect.centerx) - player.rect.width / 2
        distance_y = abs(c1.centery - player.rect.centery) - player.rect.height / 2

        # Déterminer s'il y a collision
        if distance_x ** 2 + distance_y ** 2 <= 100 ** 2:
            player.perdre_vie()

        

    for obj in tmx_data.objects:
        pos = obj.x,obj.y
        if obj.type == 'Shape':
            if obj.name == 'Marker':
                pygame.draw.circle(screen,'red',(obj.x,obj.y),5)
                
            if obj.name == 'Rectangle':
                rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                pygame.draw.rect(screen,'yellow',rect)
 
            if obj.name == 'Ellipse':
                rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                pygame.draw.ellipse(screen,'blue',rect)
 
            if obj.name == 'Polygon':
                points = [(point.x,point.y) for point in obj.points]
                pygame.draw.polygon(screen,'green',points)
"""

def checkalive():
    for player in players_group:
        if player.etat == False:
            players_group.remove(player)


def playermanage():

    for player in players_group:
        draw_text(player.role, pygame.font.Font(None, 30), BLACK, screen, player.x, player.y-80)
        
        if player.role == 'Détective':
            draw_text(str(player.bullet) + " •", pygame.font.Font(None, 30), BLACK, screen, player.x, player.y-60)

    for player in players_group:

        player.update()
        player.orientation()
        player.murder()
        player.innocent()
        player.detective()
            




def bulletsmanage():
    for player in players_group:
        for bullet in player.bulletlist:


            bullet.draw()
            bullet.move() 

            otherplayer = players_group.copy()
            otherplayer.remove(player)
            
            for player2 in otherplayer:
                if bullet.rect.colliderect(player2.rect):
                    
                    player2.perdre_vie()

            if bullet.x < 0 or bullet.x > info.current_w or bullet.y < 0 or bullet.y > info.current_h:
                player.bulletlist.remove(bullet)

            if checkcollision(bullet, layer1):
                player.bulletlist.remove(bullet)



def event():
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:
                pause_menu()


            for player in players_group:
                if e.key == pygame.K_SPACE and player.role == 'Détective' and player.bullet > 0:
                    new_bul = Bullet(player)
                    player.bullet -= 1
                    player.bulletlist.append(new_bul)


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
        tiled()
        l1g()
        checkalive()
        playermanage()
        bulletsmanage()
        winsize()
    
        pygame.display.flip()
        fpsClock.tick(fps)


#-------------------------------START-----------------------------

if __name__ == "__main__":
    main_menu()

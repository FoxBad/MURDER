
#-------------------------------IMPORT-----------------------------


import sys, os
import pygame
from pygame.locals import *
import button, image, player, bullet, redcross, sector, tile, camera
from coins import CoinsC
from pytmx.util_pygame import load_pygame


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


#-------------------------------TILED-----------------------------


tmx_data = load_pygame(os.path.join("assets", "map.tmx"))
layer1_group = pygame.sprite.Group()  # Groupe pour la première couche
layer2_group = pygame.sprite.Group()  # Groupe pour la deuxième couche

for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 128, y * 128)
            if layer.name == '1':  # Si c'est la première couche
                tile.Tile(pos=pos, surf=surf, groups=layer1_group)
            elif layer.name == '2':  # Si c'est la deuxième couche
                tile.Tile(pos=pos, surf=surf, groups=layer2_group)

    
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

innocent = pygame.image.load(os.path.join("assets", "innocent.png"))
innocent  = pygame.transform.rotate(innocent, 90)

mage = pygame.image.load(os.path.join("assets", "mage.png"))
mage  = pygame.transform.rotate(mage, 90)

assassin = pygame.image.load(os.path.join("assets", "assassin.png"))
assassin  = pygame.transform.rotate(assassin, 90)

players_group = pygame.sprite.Group()
deathgroup = pygame.sprite.Group()
coinsgroup = pygame.sprite.Group()

allsprite = pygame.sprite.Group()

CameraGroup = camera.Camera()
M1 = player.Player(100, 100, 4,pygame.K_z,pygame.K_s,pygame.K_q,pygame.K_d, allsprite, players_group, innocent, ws, hs)
CameraGroup.add(M1)

M2 = player.Player(100, 100, 4, pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT, allsprite, players_group, innocent, ws, hs)

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
    global start_ticks
    while True:

        pos = pygame.mouse.get_pos()

        winsize()

        button_x = ws // 2
        button_y = hs // 2

        fond = image.Image(ws // 2, hs // 2, "back3.jpg", (ws,hs), screen)
        
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
                    start_ticks=pygame.time.get_ticks() #starter tick
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


        fondp = image.Image(ws // 2, hs // 2, "back2.jpg", (ws,hs), screen)

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

        setfond = image.Image(ws // 2, hs // 2, "back1.jpg", (ws,hs), screen)
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
                    M1.role = "assassin"
                if button_2.rect.collidepoint(pos):
                    M1.role = "innocent"
                if button_3.rect.collidepoint(pos):
                    M1.role = "mage"

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

        setfond = image.Image(ws // 2, hs // 2, "back1.jpg", (ws,hs), screen)
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




def playermanage():
    
    CameraGroup.custom_draw(M1 , layer1_group, layer2_group, screen, allsprite)


    for p in players_group:

        p.update(layer2_group)
                
        p.roles(allsprite, ws ,hs)

        p.orientation(ws , hs )

        p.checkalive(deathgroup, allsprite)

        draw_text(str(M1.role), pygame.font.Font(None, 30), BLACK, screen, ws//2, hs//2-80)

        draw_text(str(M1.coins) + " $", pygame.font.Font(None, 30), BLACK, screen, ws//2, hs//2-60)
            
        draw_text(str(M1.vie), pygame.font.Font(None, 30), BLACK, screen, ws//2+30, hs//2-60)
        
        if p.role == 'mage':
            draw_text(str(M1.bullet) + " •", pygame.font.Font(None, 30), BLACK, screen, ws//2-30, hs//2-60)
    

def bulletsmanage():

    for player in players_group:
        for bullet in player.bulletlist:

            bullet.update()

            otherplayer = players_group.copy()
            otherplayer.remove(player)

            
            for player2 in otherplayer:
                if pygame.sprite.collide_mask(bullet, player2):
                    player2.perdre_vie()
                    bullet.kill()

            if bullet.x < 0 or bullet.x > 4400 or bullet.y < 0 or bullet.y > 4400:
                bullet.kill()

            for sprite in layer2_group:
                if pygame.sprite.collide_mask(bullet, sprite):
                    bullet.kill()
            
            if player.bullet == 0:
                player.role = 'innocent'
                player.base_img = innocent
                player.magestat = False


def coinsmanage():
    for player in players_group:
        for coin in coinsgroup:
            if pygame.sprite.collide_mask(player, coin):
                coin.kill()
                player.coins += 1
            

        if player.role != 'assassin':
            if player.coins >=10 and player.role == 'mage' and player.bullet < 3:
                player.coins -= 10
                player.bullet = 3

            if player.coins >=10 : 
                player.role = 'mage'
                player.coins -= 10
                player.bullet = 3

  
def clock():
    global start_ticks
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    if seconds>3 and len(coinsgroup) < 50 : # if more than 10 seconds close the game
        CoinsC(allsprite, coinsgroup)
        start_ticks=pygame.time.get_ticks() #starter tick

        

def event():
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
            
        
        for player in players_group:

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_ESCAPE:
                    pause_menu()

                if e.key == pygame.K_e and player.role == "assassin":
                    player.base_img = assassin
                    player.assassinstat = True
                    
                if e.key == pygame.K_r and player.role == "assassin":
                    player.base_img = innocent
                    player.assassinstat = False
                

                if e.key == pygame.K_e and player.role == "mage":
                    player.base_img = mage
                    player.magestat = True
                    
                if e.key == pygame.K_r and player.role == "mage":
                    player.base_img = innocent
                    player.magestat = False
                    


            if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and player.role == 'mage' and player.magestat == True and player.bullet > 0:
                bullet.Bullet(player, allsprite, player.bulletlist, ws ,hs)
                player.bullet -= 1
            


            if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and player.role == "assassin" and player.assassinstat == True:

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

        clock()
        playermanage()
        bulletsmanage()
        coinsmanage()
        winsize()
        event()

        pygame.display.flip()
        fpsClock.tick(fps)


#-------------------------------START-----------------------------

if __name__ == "__main__":
    main_menu()

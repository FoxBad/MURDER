
#-------------------------------IMPORT-----------------------------


import sys, os
import pygame
from pygame.locals import *
import player, bullet, tile, camera, image, button
from coins import CoinsC
from pytmx.util_pygame import load_pygame
import socket, random
import time, json


#---------------------------INIT PYGAME-------------------------
pygame.init()

fps = 120
fpsClock = pygame.time.Clock()

info = pygame.display.Info()
w = 600
h = 800

global MAX_PLAYERS
MAX_PLAYERS = 3

pygame.display.set_caption("APEO - BETA")
icon = pygame.image.load(os.path.join("assets", "logo2.png"))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((w, h), RESIZABLE)

def winsize():
    global ws, hs
    ws, hs = screen.get_size()

winsize()

#---------------------------INIT SERVER--------------------------


HOST = '192.168.56.1'
PORT = 5050


#---------------------------INIT SERVER--------------------------

def initserv():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

#-------------------------------TILED-----------------------------


tmx_data = load_pygame(os.path.join("assets", "map.tmx"))
layer1_group = pygame.sprite.Group()  # Groupe pour la première couche
layer2_group = pygame.sprite.Group()  # Groupe pour la deuxième couche

for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 128, y * 128)
            if layer.name == 'Tile Layer 1':  # Si c'est la première couche
                tile.Tile(pos=pos, surf=surf, groups=layer1_group)
            elif layer.name == 'Tile Layer 2':  # Si c'est la deuxième couche
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
                    initserv()
                    sync()

                if quit_button.rect.collidepoint(pos):
                    tryquit()



            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((w, h))
                    else:
                        pygame.display.set_mode((1920, 1080), FULLSCREEN)


        pygame.display.update()


#---------------------------SEND/RECEIVE FUNCTION----------------------
    

#fonction to send data
def send_update():
    update = json.dumps(P.data)
    client.send(update.encode())

def receive_message():
    global other_player_data
    message = client.recv(4096).decode()

    if message:
        try:

            data = json.loads(message)
            other_player_data = data

            del other_player_data[str(P.playerid)]


        except json.JSONDecodeError as e:
            print("JSON decoding error:", e)
    else:
        print("Empty message received")

#-------------------------------JEU-----------------------------

def updateotherplayer():
    
    
    P.currentPlayer = len(other_player_data)

    i = 0

    global rx, ry

    for key in other_player_data:
        
        if key == "rcoins":

            rx = other_player_data[key][0]
            ry = other_player_data[key][1]

        else:
            for key2 in other_player_data[key]:
            
                setattr(opgroup[i], key2, other_player_data[key][key2])

            i+=1


    
    

        
    
def sync():
    global players_group,deathgroup, coinsgroup, allsprite, CameraGroup, P, opgroup

    #Load id for main player 
    pre = client.recv(4096).decode()
    predatas = json.loads(pre)


    id = list(predatas.values())[0]
    role = list(predatas.values())[1]
    

    players_group = pygame.sprite.Group()
    deathgroup = pygame.sprite.Group()
    coinsgroup = pygame.sprite.Group()
    allsprite = pygame.sprite.Group()
    CameraGroup = camera.Camera()
    opgroup = []

    P = player.Player(allsprite, players_group, ws, hs, True, id , role)

    CameraGroup.add(P)


    for i in range(1, MAX_PLAYERS):
        opgroup.append(player.Player(allsprite, players_group, ws, hs, False, None, None))

        

    syncing = True
    while syncing:

        winsize()

        screen.fill(BLACK)

        draw_text("WAITING FOR PLAYERS", pygame.font.Font(None, 50), WHITE, screen, ws//2, hs//2)
        draw_text(str(P.currentPlayer)+ "/"+ str(MAX_PLAYERS), pygame.font.Font(None, 50), WHITE, screen, ws//2, hs//2+50)

        send_update()
        receive_message()

        P.currentPlayer = len(other_player_data)

        i = 0

        for key in other_player_data:

                        
            if len(other_player_data[key]) < 10:
                pass 
            
            else:


                for key2 in other_player_data[key]:
                    setattr(opgroup[i], key2, other_player_data[key][key2])
                i+=1

                
                

                if i == MAX_PLAYERS-1:
                    P.data["state"] = "INGAME"

                    syncing = False
                    game()


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
        
        
    


def playermanage():
    
    CameraGroup.custom_draw(P , layer1_group, layer2_group, screen, allsprite)


    for p in players_group:

        p.update(layer2_group)
                
        p.roles(allsprite, ws ,hs)

        p.orientation(ws , hs )

        p.checkalive(deathgroup, allsprite)

        p.isshoot(players_group, allsprite, ws, hs)

        P.update_data()


    draw_text(str(P.role), pygame.font.Font(None, 30), BLACK, screen, ws//2, hs//2-80)

    draw_text(str(P.coins) + " $", pygame.font.Font(None, 30), BLACK, screen, ws//2, hs//2-60)
        
    draw_text(str(P.vie), pygame.font.Font(None, 30), BLACK, screen, ws//2+30, hs//2-60)
    
    if P.role == 'mage':
        draw_text(str(P.bullet) + " •", pygame.font.Font(None, 30), BLACK, screen, ws//2-30, hs//2-60)
    

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

            if bullet.x < 0 or bullet.x > 9600 or bullet.y < 0 or bullet.y > 9600:
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
        CoinsC(allsprite, coinsgroup, rx, ry)
        start_ticks=pygame.time.get_ticks() #starter tick

                 
        

def event():
            
    for e in pygame.event.get():

        if e.type == QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_e and P.role == "assassin":
                P.assassinstat = True
            if e.key == pygame.K_r and P.role == "assassin":
                P.assassinstat = False
            

            if e.key == pygame.K_e and P.role == "mage":
                P.magestat = True
            if e.key == pygame.K_r and P.role == "mage":
                P.magestat = False
                    


        if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and P.role == 'mage' and P.magestat == True and P.bullet > 0:
            P.isshooting = True


        if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and P.role == "assassin" and P.assassinstat == True:
            P.isshooting = True
                        

#-----------------------------MAIN GAME LOOP-----------------------------

# Game loop.
def game():
    running = True

    while running:  
        screen.fill(WHITE)
        winsize()

        P.update_data()

        send_update()
        receive_message()

        updateotherplayer()

        clock()
        playermanage()
        bulletsmanage()
        coinsmanage()
        

        event()

        pygame.display.flip()
        fpsClock.tick(fps)


#-------------------------------START-----------------------------

if __name__ == "__main__":
    main_menu()

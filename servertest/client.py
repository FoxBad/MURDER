
#-------------------------------IMPORT-----------------------------


import sys, os
import pygame
from pygame.locals import *
import player, bullet, tile, camera
from coins import CoinsC
from pytmx.util_pygame import load_pygame
import socket, random
import time, json


#---------------------------INIT PYGAME-------------------------
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

#---------------------------INIT SERVER--------------------------


HOST = '192.168.1.18'
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


#---------------------------INIT SERVER--------------------------

#Load id for main player 
id = client.recv(4096).decode()
data_playerid = json.loads(id)

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

P = player.Player(allsprite, players_group, innocent, ws, hs, True, data_playerid)

CameraGroup.add(P)

P2 = player.Player(allsprite, players_group, innocent, ws, hs, False, None)

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
        
    for key in other_player_data:

        P2.playerid = other_player_data[key]["playerid"]
        P2.pos = other_player_data[key]["pos"]
        P2.mpos = other_player_data[key]["mpos"]
        P2.role = other_player_data[key]["role"]
        P2.assassinstat = other_player_data[key]["assassinstat"]
        P2.magestat = other_player_data[key]["magestat"]
        P2.etat = other_player_data[key]["etat"]


        
    
def sync():

    syncing = True
    while syncing:

        send_update()
        receive_message()
        

        for key in other_player_data:
                        
            if len(other_player_data[key]) < 8:
                pass
            
            else:

                P2.playerid = other_player_data[key]["playerid"]
                P2.pos = other_player_data[key]["pos"]
                P2.mpos = other_player_data[key]["mpos"]
                P2.role = other_player_data[key]["role"]
                P2.assassinstat = other_player_data[key]["assassinstat"]
                P2.magestat = other_player_data[key]["magestat"]
                P2.etat = other_player_data[key]["etat"]

                P.data["state"] = "INGAME"

                syncing = False




def playermanage():
    
    CameraGroup.custom_draw(P , layer1_group, layer2_group, screen, allsprite)


    for p in players_group:

        p.update(layer2_group)
                
        p.roles(allsprite, ws ,hs)

        p.orientation(ws , hs )

        p.checkalive(deathgroup, allsprite)

        p.update_data()


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
            
        
        if e.type == pygame.KEYDOWN:


            if e.key == pygame.K_e and P.role == "assassin":
                P.base_img = assassin
                P.assassinstat = True
            if e.key == pygame.K_r and P.role == "assassin":
                P.base_img = innocent
                P.assassinstat = False
            

            if e.key == pygame.K_e and P.role == "mage":
                P.base_img = mage
                P.magestat = True
            if e.key == pygame.K_r and P.role == "mage":
                P.base_img = innocent
                P.magestat = False
                


        if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and P.role == 'mage' and P.magestat == True and P.bullet > 0:
            bullet.Bullet(P, allsprite, P.bulletlist, ws ,hs)
            P.bullet -= 1
        


        if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and P.role == "assassin" and P.assassinstat == True:
            otherplayer = players_group.copy()
            otherplayer.remove(P)
            
            for player2 in otherplayer:
                if pygame.sprite.collide_mask(P.sector, player2):
                    player2.perdre_vie()
                    

#-----------------------------MAIN GAME LOOP-----------------------------

# Game loop.
def game():
    running = True

    sync()

    while running:
       
        send_update()
        receive_message()

        updateotherplayer()

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
    start_ticks=pygame.time.get_ticks() #starter tick
    game()

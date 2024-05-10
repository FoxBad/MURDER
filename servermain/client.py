import socket, random
import time
import sys
import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
 

def read_pos(str):
    str = str.split(",")
    for str1 in str:
        if str1 != "":
            str1 = str1.split(":")
            pos = str1[1].split(" ")
            other_player_pos[str1[0]] = (int(pos[0]), int(pos[1]))
    return other_player_pos

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.pos =  (0, 0)




        
HOST = '172.20.10.2'
PORT = 5050
position = str(random.randint(0,100)) + " " + str(random.randint(0,100))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
other_player_pos = {}


pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))


 
# Game loop.
while True:
  
    # Envoyer la position au serveur
    client.send(position.encode())
    # Recevoir la position des autres clients
    other_positions = client.recv(2048).decode()
    print(f"Positions des autres clients : {read_pos(other_positions)}")
    
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Draw.
    
    pygame.display.flip()
    fpsClock.tick(fps)
# Adresse IP et port du serveur









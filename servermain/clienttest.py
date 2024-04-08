import socket, random
import time

# Adresse IP et port du serveur
HOST = '192.168.1.21'
PORT = 5050

position = str(random.randint(0,100)) + " " + str(random.randint(0,100))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

other_player_pos = {}

def read_pos(str):
    str = str.split(",")
    for str1 in str:
        if str1 != "":
            str1 = str1.split(":")
            pos = str1[1].split(" ")
            other_player_pos[str1[0]] = (int(pos[0]), int(pos[1]))
    return other_player_pos

while True:

    time.sleep(1)

    # Envoyer la position au serveur
    client.send(position.encode())

    # Recevoir la position des autres clients
    other_positions = client.recv(2048).decode()
    
    print(f"Positions des autres clients : {read_pos(other_positions)}")

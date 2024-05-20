import socket, random
import time, sys, json

HOST = '192.168.56.1'
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class Player():
    def __init__(self, playerid):
        self.x = random.randint(0,1000)
        self.y = random.randint(0,1000)
        self.pos = self.x, self.y
        self.playerid = playerid
        self.data = {"playerid" : self.playerid ,"position": self.pos}


#Load id for main player 
id = client.recv(4096).decode()
data = json.loads(id)

#creating player
P = Player(data)

#fonction to send data
def send_update():
    update = json.dumps(P.data)
    client.send(update.encode())

def receive_message():
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

while True:
    
    send_update()
    receive_message()

    

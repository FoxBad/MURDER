import socket, random
import time, sys, json

HOST = '192.168.56.1'
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class Player():
    def __init__(self, playerid):
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 1000)
        self.pos = self.x, self.y
        self.playerid = playerid

id = client.recv(4096).decode()
data = json.loads(id)
P = Player(data)

def send_update():
    update = json.dumps({"playerid": P.playerid, "position": P.pos})
    client.send((update + '\n').encode())

def receive_message():
    message = client.recv(4096).decode()
    if message:
        try:
            data = json.loads(message)
            other_player_data = data

            for i in other_player_data:
                if i == P.playerid:
                    del other_player_data[i]

        except json.JSONDecodeError as e:
            print("JSON decoding error:", e)
    else:
        print("Empty message received")

while True:
    send_update()
    receive_message()
    time.sleep(1)

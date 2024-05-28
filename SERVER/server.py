import socket
import threading, json, random

clients = []
players = {}
roles = ["Assassin", "Innocent", "Mage"]
spawns = [(8000, 3200), (6500, 6700), (1600, 1000)]


coins = []
for i in range(0,500):
    coins.append((random.randint(0, 9600), random.randint(0, 9600)))

# Configuration du serveur
HOST = '192.0.0.2'
PORT = 5050
currentPlayer = 0
MAX_PLAYERS = 3
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_PLAYERS) # Limite de 2 clients

print(f"Serveur en écoute sur {HOST}:{PORT}")



# Fonction pour gérer les connexions des clients
def handle_client(client_socket, client_address):
    global currentPlayer

    print(f"Connexion acceptée de {client_address}")


    role = random.choice(roles)
    roles.remove(role)

    spawn = random.choice(spawns)
    spawns.remove(spawn)

    sent = json.dumps({"playerid" : client_address[1], "role" : role, "pos" : spawn})
    client_socket.send(sent.encode())
    
    players[client_address[1]] = {}

    k=0

    try:
        while True:
            
            # Recevoir la position du client
            receive = client_socket.recv(4096).decode()

            if not receive:
                break

            data = json.loads(receive)

            players[client_address[1]] = data


            if players[client_address[1]]["state"] == "READY":
                k+=1

            players["rcoins"] = coins[k]

            # Redistribuer la position à tous les clients connectés
            sent = json.dumps(players)
            client_socket.send(sent.encode())

    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        client_socket.close()
        currentPlayer -= 1
        roles.append(role)
        spawns.append(spawn)
        del players[client_address[1]]
        print(f"Connexion avec {client_address} fermée")


while True:
    # Accepter les connexions des clients
    client_socket, client_address = server.accept()
    clients.append((client_socket,client_address))

    currentPlayer += 1
    print(f"Joueur connecté. Nombre total de joueurs: {currentPlayer}/{MAX_PLAYERS}")

    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

import socket
import threading, time, json

clients = []
players = {}

# Configuration du serveur
HOST = '192.168.1.18'
PORT = 5050
currentPlayer = 0
MAX_PLAYERS = 2
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_PLAYERS) # Limite de 2 clients

print(f"Serveur en écoute sur {HOST}:{PORT}")

# Fonction pour gérer les connexions des clients
def handle_client(client_socket, client_address):
    global currentPlayer

    print(f"Connexion acceptée de {client_address}")

    sent = json.dumps(client_address[1])
    client_socket.send(sent.encode())
    players[client_address[1]] = {'playerid': client_address[1]}

    try:
        while True:

            # Recevoir la position du client
            receive = client_socket.recv(4096).decode()

            if not receive:
                break

            data = json.loads(receive)

            players[client_address[1]] = data

            # Redistribuer la position à tous les clients connectés
            sent = json.dumps(players)
            client_socket.send(sent.encode())

    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        client_socket.close()
        currentPlayer -= 1
        del players[client_address[1]]
        print(f"Connexion avec {client_address} fermée")


while True:
    # Accepter les connexions des clients
    client_socket, client_address = server.accept()
    clients.append((client_socket,client_address))

    currentPlayer += 1
    print(f"Joueur connecté. Nombre total de joueurs: {currentPlayer}/{MAX_PLAYERS}")

    if currentPlayer == MAX_PLAYERS:
        time.sleep(5)
        for client, address in clients:
            threading.Thread(target=handle_client, args=(client, address)).start()

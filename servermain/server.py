import socket
import threading, time


# Fonction pour gérer les connexions des clients
def handle_client(client_socket, client_address):
    print(f"Connexion acceptée de {client_address}")
    while True:
        
        time.sleep(1)
        try:
            # Recevoir la position du client
            position = client_socket.recv(2048).decode()
            print(f"Position reçue de {client_address}: {position}")

            # Redistribuer la position à tous les clients connectés
            for c in clients:
                if c != client_socket:
                    c.send((str(client_address[1]) + ':' + position + ',').encode())
                    #c.send((position + ',').encode())
        except Exception as e:
            print(f"Erreur: {e}")
            break

    # Fermer la connexion avec le client
    client_socket.close()
    print(f"Connexion avec {client_address} fermée")

# Configuration du serveur
HOST = '192.168.56.1'
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(3)  # Limite de 3 clients

print(f"Serveur en écoute sur {HOST}:{PORT}")

clients = []
currentPlayer = 0

while True:
    # Accepter les connexions des clients
    client_socket, client_address = server.accept()
    clients.append(client_socket)
    currentPlayer += 1


    # Démarrer un thread pour gérer la connexion du client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

import socket
import threading
import pickle
import random


nb = int(input(" combien de joueurs ? "))
PLAYER_SPEED = int ( input ( "vitesse ?"))
game_over = False
cells = []
matriceSize = (1000,1000)
# Fonction pour gérer la communication entre deux clients
def handle_client(client_socket, other_client):
    while True:
        print("1")
        data = client_socket.recv(1024)
        if not data:
            break
        rep = pickle.loads(data)
        id = rep["id"]
        direction = rep["direction"]
        for n in range(len(clients)):
            print(clients[n][2])
            if clients[n][2] == id :
                rang = n

        # déterminer les cases altérées 
        new_cells = []
        for n in range (1,PLAYER_SPEED +1):
            print(rang)
            new_cell = (clients[rang][4][0] + direction[0] *n , clients[rang][4][1] + direction[0] *n)
            new_cells.append(new_cell)
            if new_cell in cells:
                game_over = True 
            else:
                cells.append (new_cell)

        # Déterminer la nouvelle position
        clients[rang][4] = [clients[rang][4][0] + direction[0] *PLAYER_SPEED , clients[rang][4][1] + direction[0] *PLAYER_SPEED]
        if not 0 < clients[rang][4][0] < matriceSize[0] :
                game_over = True
        if not 0 < clients[rang][4][1] < matriceSize[1] :
                game_over = True
        
        transmission  = {"new_cells" : new_cells, "color" : clients[rang][3]}
        for client in other_client :
            if client != client_socket:
                client.send(pickle.dumps(transmission))

def couleur_aleatoire():
    r = random.randint(0, 200)
    g = random.randint(0, 200)
    b = random.randint(0, 200)

    return (r, g, b)


# Créer un socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # Ecoute sur toutes les interfaces sur le port 12345
server.listen(nb)

print("[*] Serveur en attente de connexions...")

# Attendre connexions de clients
clients=[]
for x in range(nb):
    client, addr = server.accept()
    print(f"[*] Connexion acceptée de : {addr[0]}:{addr[1]}")
    id = x
    color = couleur_aleatoire()
    position = [random.randint(0,matriceSize[0]),random.randint(0,matriceSize[1])]
    clients.append([client,addr,id,color,position])

# Synchro 
for client in clients:
    client[0].send(True.to_bytes(1, byteorder='big'))#envoie True pour commencer la boucle while
    client[0].send(client[2].to_bytes(4,byteorder = 'big') ) # envoie l'id 
    client[0].send(nb.to_bytes(4,byteorder = 'big') )    

# Démarrer les threads pour gérer la communication entre les clients
threads = []

# Supposons que vous avez une liste de clients, chaque élément est un tuple (client, addr , id , color)
for i in range(nb):
    other_clients = [client[0] for client in clients if client[0] != clients[i][0]]
    print(other_clients[0])
    t = threading.Thread(target=handle_client, args=(clients[i][0], other_clients))
    threads.append(t)
    t.start()

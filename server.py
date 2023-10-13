import socket
import threading

# Fonction pour gérer la communication entre deux clients
def handle_client(client_socket, other_client):
    while True:
        data = client_socket.recv(1024)
        if not data:
            print("Stopitotototo")
            break
        print(data)
        other_client.send(data)

# Créer un socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # Ecoute sur toutes les interfaces sur le port 8080
server.listen(5)

print("[*] Serveur en attente de connexions...")

# Attendre deux connexions de clients
client1, addr1 = server.accept()
print(f"[*] Connexion acceptée de : {addr1[0]}:{addr1[1]}")
client2, addr2 = server.accept()
print(f"[*] Connexion acceptée de : {addr2[0]}:{addr2[1]}")

# Synchro 
client1.send(True.to_bytes(1, byteorder='big'))
client2.send(True.to_bytes(1, byteorder='big'))

# Démarrer deux threads pour gérer la communication entre les clients
t1 = threading.Thread(target=handle_client, args=(client1, client2))
t2 = threading.Thread(target=handle_client, args=(client2, client1))

t1.start()
t2.start()

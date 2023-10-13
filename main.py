import pygame
import socket
import pickle
import random





# Paramètres du client
SERVER_HOST = '172.21.72.133'  # Adresse IP du serveur
SERVER_PORT = 12345  # Port du serveur

"""
# Paramètres du jeu
FPS_UPDATE = 100  # Taux de mise à jour du jeu (en Hz)
FPS_RENDER = 60   # Taux de rendu de la matrice (en Hz)
"""
MATRIX_SIZE = (1000, 1000)  # Taille de la matrice
 # Vitesse du joueur (*FPS_UPDATE)

# Initialisation de Pygame
pygame.init()

# Créez une fenêtre Pygame pour l'affichage
WINDOW = pygame.display.set_mode(MATRIX_SIZE)
pygame.display.set_caption("Light Racer")
"""
# Horloge pour contrôler la fréquence de mise à jour et de rendu
update_clock = pygame.time.Clock()
render_clock = pygame.time.Clock()
"""
# Créez une socket pour le client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running = False
try:
    # Connectez-vous au serveur
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connecté au serveur {SERVER_HOST}:{SERVER_PORT}")

    bool_data = client_socket.recv(1)
    print("1")
    if bool(int.from_bytes(bool_data, byteorder='big')):
        running = True
        print(running)
        id = int.from_bytes(client_socket.recv(4), byteorder='big')
        nb = int.from_bytes(client_socket.recv(4), byteorder='big')
        print(nb)
    direction = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
    while running:
                # Gestion des touches
        print("2")
        touches = pygame.key.get_pressed()
        
        if touches[pygame.K_z]:
            direction = ( 0, -1)
        if touches[pygame.K_s]:
            direction = ( 0, 1)
        if touches[pygame.K_q]:
            direction = ( -1, 0)
        if touches[pygame.K_d]:
            direction = ( 1, 0)

        transmission = {"id" : id , "direction"  : direction}
        print(transmission)
        serialized_data = pickle.dumps(transmission)

        # Envoyez les données au serveur
        print("2")
        client_socket.send(serialized_data)
        print("1")

        # Affichage
        for x in range(nb):
            print("4")
            data = client_socket.recv(1024)
            print("3")
            data = pickle.loads(data)
            print("3")
            for cell in data["new_cells"]:
                pygame.draw.rect(WINDOW, data["color"], (cell[0], cell[1], 3, 3))  # Dessinez les cases modifiées
        pygame.display.flip()



except Exception as e:
    print(f"Erreur lors de la communication avec le serveur: {str(e)}")

finally:
    # Fermez la connexion client
    client_socket.close()




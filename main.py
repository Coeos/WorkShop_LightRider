# main.py
import pygame
from game import Game
from player import Player
import keyboard
import socket
import pickle

# Paramètres du client
SERVER_HOST = '172.21.72.133'  # Adresse IP du serveur
SERVER_PORT = 12345  # Port du serveur


# Paramètres du jeu
FPS_UPDATE = 100  # Taux de mise à jour du jeu (en Hz)
FPS_RENDER = 60   # Taux de rendu de la matrice (en Hz)
MATRIX_SIZE = (1000, 1000)  # Taille de la matrice
PLAYER_SPEED = 4  # Vitesse du joueur (*FPS_UPDATE)

# Initialisation de Pygame
pygame.init()

# Créez une instance de la classe Game
game = Game(MATRIX_SIZE, PLAYER_SPEED, FPS_UPDATE)

# Créez deux instances de la classe   Player
player1 = Player(id = 1, player_position=( MATRIX_SIZE[0] // 3, 2 * MATRIX_SIZE[1] // 3))
player2 = Player(id = 2, player_position=( 2 * MATRIX_SIZE[0] // 3, MATRIX_SIZE[1] // 3))

# Créez une fenêtre Pygame pour l'affichage
WINDOW = pygame.display.set_mode(MATRIX_SIZE)
pygame.display.set_caption("Light Racer")

# Horloge pour contrôler la fréquence de mise à jour et de rendu
update_clock = pygame.time.Clock()
render_clock = pygame.time.Clock()


# Créez une socket pour le client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connectez-vous au serveur
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connecté au serveur {SERVER_HOST}:{SERVER_PORT}")

    ite = 0
    bool_data = client_socket.recv(1)
    if bool(int.from_bytes(bool_data, byteorder='big')):
        running = True
    while running:
        ite +=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Partie serveur 
        print(ite)

        # création de la transmission
        transmission = {
        "player_id": 1,
        "position": player1.player_position,  # Position du joueur
        "direction": player1.direction  # Direction du joueur
        }

        # Ensuite, sérialisez les données à l'aide de pickle pour les envoyer au serveur
        serialized_data = pickle.dumps(transmission)

        # Envoyez les données au serveur
        client_socket.send(serialized_data)
        print(ite)
        # Attendez une réponse du serveur (si nécessaire)
        response_data = client_socket.recv(1024)

        # Désérialisez les données de réponse à l'aide de pickle
        rep = pickle.loads(response_data)      

        player2.set_direction(rep["direction"])
        player2.set_position(rep["position"])

        print(rep["direction"])
        print(rep["position"])



        # Partie Jeu

        # Gestion de l'input du joueur
        keyboard.add_hotkey('z',player1.haut)
        keyboard.add_hotkey('q',player1.gauche)
        keyboard.add_hotkey('s',player1.bas )
        keyboard.add_hotkey('d',player1.droite)
        print(ite)
        # Mise à jour de l'état du jeu
        player1.player_position = game.update(player_direction = player1.direction , player_position = player1.player_position)
        print(ite)
        
        # Rendu de la matrice
        new_changed_cells = game.get_new_changed_cells()
        for cell in new_changed_cells:
            pygame.draw.rect(WINDOW, (0, 0, 255), (cell[0], cell[1], 1, 1))  # Dessinez les cases modifiées

        print(str(game.get_game_over))
        # Mise à jour de l'état du jeu
        game.update(player_direction = player2.direction , player_position = player2.player_position)
        ### Vérifier que player position envoyé est bioen celle trouvé à la fin de cette fonction



        # Rendu de la matrice
        new_changed_cells = game.get_new_changed_cells()
        for cell in new_changed_cells:
            pygame.draw.rect(WINDOW, (255, 0, 0), (cell[0], cell[1], 1, 1))  # Dessinez les cases modifiées
        
        # Mettez à jour l'affichage
        pygame.display.flip()


        # Attendez pour atteindre la fréquence de mise à jour
        pygame.time.delay(int(1000 / FPS_UPDATE))

 
        print(str(game.get_game_over))
    pygame.quit()
except Exception as e:
    print(f"Erreur lors de la communication avec le serveur: {str(e)}")

finally:
    # Fermez la connexion client
    client_socket.close()
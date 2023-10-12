# game.py
import pygame


class Game:
    def __init__(self, matrix_size, player_speed,fps_update):
        # Initialisez la classe Game
        self.matrix_size = matrix_size
        self.player_speed = player_speed
        self.fps_update = fps_update
        self.changed_cells = []
        self.new_changed_cells = []
        self.game_over = False
        

    def update(self, player_direction,player_position):
        if not self.game_over :
            #ré-initialisé les nouvelles cellules changées 
            self.new_changed_cells = []

            # Calculez la nouvelle position du joueur en fonction de sa direction et de sa vitesse
            delta_x = player_direction[0] * self.player_speed
            delta_y = player_direction[1] * self.player_speed

            # Trouver les cases changées
            for _ in range(self.player_speed):
                self.new_changed_cells.append((player_position[0] + _*player_direction[0] , player_position[1] + _*player_direction[1]))
        
            # Mettez à jour la position du joueur
            player_position = [player_position[0] + delta_x, player_position[1] + delta_y]

            
            # Assurez-vous que le joueur reste à l'intérieur de la matrice
            if not 0 < player_position[0] < self.matrix_size[0] :
                self.game_over = True
            if not 0 < player_position[1] < self.matrix_size[1] :
                self.game_over = True
            
            
            # Ajoutez la case modifiée par le joueur à l'ensemble
            for a in self.new_changed_cells :
                if a in self.changed_cells:
                    self.game_over = True
                else:
                   self.changed_cells.append(a)
            return player_position
        else:
            pygame.quit()
            
    def get_changed_cells(self):
        return self.changed_cells
    
    def get_new_changed_cells(self):
        return self.new_changed_cells
    
    def get_game_over(self):
        return self.game_over
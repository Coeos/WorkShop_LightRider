# player.py
import pygame
import keyboard

class Player:
    def __init__(self,id,player_position):
        # Initialisez la classe Player
        self.id = id

        # Position initiale 
        self.player_position = player_position
        # Direction initiale
        if id == 1:
            self.direction = (0, -1)
        elif id == 2:
            self.direction = (0, 1)
        elif id == 3:
            self.direction = (-1,0)
        elif id == 4 :
            self.direction = (1,0)
        else :
            self.direction = ( 0 ,-1)

    def haut(self):
        if self.direction != (0,1):
            self.direction = (0 , -1)

    def bas(self):
        if self.direction != (0,-1):
            self.direction = (0 , 1)

    def gauche(self):
        if self.direction != (1,0):
            self.direction = (-1 , 0)

    def droite(self):
        if self.direction != (-1,0):
            self.direction = (1 , 0)

    def get_direction(self):
        return self.direction   
    
    def get_id (self):
        return self.id
    
    def set_direction(self,direction):
        self.direction = direction
    
    def set_position(self,position):
        self.player_position = position
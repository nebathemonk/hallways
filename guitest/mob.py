import pygame
import string

class Mob(object):
    def __init__(self):
        self.locx = 0; self.locy = 0 #location variables for drawing the mob on screen
        self.name = "";
        self.image = None; #the file used for drawing the mob
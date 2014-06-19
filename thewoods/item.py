import curses
from mob import *
from map import *
from config import *

class ITEM(object):
    
    def __init__ (self,type):
        self.name = "Item"; self.type = "item" #type is for creating/using, name is for display
        self.damage = 0; self.damage_rating = "low"
        self.range = 1; self.range_rating = "personal"
        self.icon = "/"; self.color = 1
        self.selected = 0 #flag for selected in inventory loop
        self.held = 0 #so we know to draw it on ground or not
        self.locx = 0; self.locy = 0 #location variabls for when on the ground
        self.setitem(type)
    
    def setitem(self,type):
        if type == "chainsaw":
            self.name = "Chainsaw"
            self.damage = 100; self.damage_rating = "high"
            self.range = 1; self.range_rating = "personal"
            self.icon = "p"; self.color = 6 #white
            
        elif type == "medkit":
            self.name = "Medical Kit"
            self.damage = 10; self.damage_rating = "low"
            self.range = 1; self.range_rating = "personal"
            self.icon = "+"; self.color = 4 #red
        
        elif type == "handgun":
            self.name = "9MM handgun"
            self.damage = 66; self.damage_rating = "med"
            self.range = 5; self.range_rating = "short"
            self.icon = "r"; self.color = 5 #purple
        
        elif type == "baton":
            self.name = "Baton"
            self.damage = 66; self.damage_rating = "med"
            self.range = 1; self.range_rating = "personal"
            self.icon = ","; self.color = 6 #cyan
            
        elif type == "zombie":
            self.name = "mauls"
            self.damage = 33; self.damage_rating = "low"
            self.range = 1; self.range_rating = "personal"
            self.icon = ","; self.color = 4 #red
            
        elif type == "corpse":
            self.name = "corpse"
            self.damage = 10; self.damage_rating = "what?"
            self.range = 1; self.range_rating = "gross!"
            self.icon = "%"; self.color = 4 #red
            
        else:
            self.name = "Item"
            self.damage = 0; self.damage_rating = "low"
            self.range = 1; self.range_rating = "personal"
            self.icon = "/"; self.color = 1
    
    def activate(self,user):
        if self.name == "Medical Kit":
            activationtext = "Medkit used."
            user.health += 33 #heal the user by 33 points (should change based on medkit skill, etc)
        
        else:
            activationtext = "How you do "+self.name+"?"
        return activationtext
    
    
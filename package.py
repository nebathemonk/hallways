from mob import Mob
from skill import skill
from weapon import weapon
import random

#///////////////Skills//////////////////////////
class slash(skill):    
    def __init__(self):
        skill.__init__(self)
        self.name = "Slash"
        self.type = "offense"
        self.damage = 2; self.stamina = 1.11; 
        
    def on_use(self,player,weapon):
        print self.name+" causes the target to bleed"
        damage = skill.on_use(self,player,weapon)
        return damage
        
        
class flurry(skill):    
    def __init__(self):
        skill.__init__(self)
        self.name = "Flurry of Blows"
        self.type = "offense"
        self.damage = 1; self.stamina = 1.33
        self.hits = 4 #incase failure of get_hits
    
    def on_use(self,player,weapon):
        print self.name+" tenderizes the target!"
        damage = (skill.on_use(self,player,weapon)/2)
        return damage
        
#//////////////////////////Weapons//////////////////////
class sword_short(weapon):
    def __init__(self):
        weapon.__init__(self)
        self.name = "Short Sword"
        self.damage = 2; self.level = 5
        
        skill1 = slash() #give the player slash if they equip item
        skill2 = flurry()
        self.skills = [skill1,skill2]

#////////////////////////mobs//////////////////////////////
class dummy(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.name = "Dummy Target"
        self.job = "target"        
        self.defense = 100; self.speed = 1

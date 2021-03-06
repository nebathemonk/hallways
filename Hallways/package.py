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
        self.damage = 2; self.stamina = 0.15; 
        
    def on_use(self,player,weapon):
        print self.name+" causes the target to bleed"
        damage = skill.on_use(self,player,weapon)
        return damage
        
        
class flurry(skill):    
    def __init__(self):
        skill.__init__(self)
        self.name = "Flurry of Blows"
        self.type = "offense"
        self.damage = 1; self.stamina = 0.20
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

class Goblin(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.name = "Goblin"
        self.job = "Scrappy Danger"
        self.speed = 1
        
        self.image = 'goblin.png'
        
# Definitions of all of the character mobs
class Bob(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.name = "Bob"; self.job = "Bee Keeper"
        self.speed = 2 #speed, init for turn order
        self.dead = 0 #use for taking out of combat
        #self.weapon = None #currently equiped weapon
        self.team = 1 #team 1 is players, team 2 is AI
        self.skills = [] #list of skills for mob, based on equipment
        self.growth_attack = 1; self.growth_defense = 0.89; self.growth_accuracy = 1.33
        self.growth_evasion = 1.22; self.growth_health = 0.89; self.growth_stamina = 1.11
        
        self.image = 'knight3.png'

class Sarah(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.name = "Sarah"; self.job = "Secret Sulfate"
        self.speed = 2 #speed, init for turn order
        self.dead = 0 #use for taking out of combat
        #self.weapon = None #currently equiped weapon
        self.team = 1 #team 1 is players, team 2 is AI
        self.skills = [] #list of skills for mob, based on equipment
        self.growth_attack = 1.11; self.growth_defense = 0.89; self.growth_accuracy = 1.22
        self.growth_evasion = 1; self.growth_health = 0.89; self.growth_stamina = 1.22

        self.image = 'knight3.png'

        

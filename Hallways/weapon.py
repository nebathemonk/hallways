import skill
import mob

class weapon(object):
    def __init__(self):
        self.name = "weapon"
        self.damage = 1; self.level = 1
        self.skills = [] #the skill the weapom gives
        
    def get_damage(self): return self.damage

    def on_equip(self): return self.skills #give the weapons skills to the player that equips it


        
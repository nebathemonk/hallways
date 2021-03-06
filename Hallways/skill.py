import random
import weapon
import mob

class skill(object):
    def __init__(self):
        self.name = "skill"
        self.type = "offense" #offense, defense, self
        self.damage = 1; self.dmgmin = 0.75; self.dmgmax = 1.25
        self.stamina = 0.15; self.hits = 1 #the number of attacks per use, percentage of total stamina use
        self.accuracy = 1; self.targets = 1 #the number of targeted mobs for skill use
        
        self.skillnumber = 0;
        self.image = 'skill.png' #number is the slot it is in. image is its icon 32x32
    
    def get_damage(self): return self.damage
    def get_hits(self): return self.hits
    def get_stamina(self): return self.stamina
    def get_level(self): return self.level
    
    def get_type(self): return self.type

    def on_use(self,player,weapon):
        #damage = 0
        if(self.type == "offense"):
            attack = player.get_attack()
            sdamage = self.get_damage()
            wdamage = weapon.get_damage()
            levelmod = float(player.level)/float(weapon.level)
            damagemin = int(((attack*self.dmgmin)*wdamage)*sdamage)
            damagemax = int(((attack*self.dmgmax)*wdamage)*sdamage)
            damage = int((random.randrange(damagemin,damagemax)*levelmod))
            print "damage from attack: "+str(damagemin)+"/"+str(damagemax)
            return damage
        else: pass
    
    def use_stamina(self,player,weapon):
        levelmod = float(player.level) / float(weapon.level) #changes stamina percent based on level difference
        userstamina = player.get_stamina()
        skillstamina = self.stamina*levelmod
        staminause = int(userstamina*skillstamina)
        player.stamina -= staminause
        print self.name+" uses "+str(staminause)+" stamina, leaving"+str(player.stamina)


        
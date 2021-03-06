import weapon
import skill

class Mob(object):
    def __init__(self):
        self.name = "mob"
        self.job = "class"
        self.attack = 50; self.defense = 50; self.accuracy = 50; self.evasion = 50
        self.health = 100; self.stamina = 100; self.level = 1; self.speed = 3 #speed, init for turn order
        self.maxhealth = 100; self.maxstamina = 100
        self.dead = 0 #use for taking out of combat
        self.weapon = None #currently equiped weapon
        self.team = 2 #team 1 is players, team 2 is AI
        self.skills = [] #list of skills for mob, based on equipment
        self.exp = 0; self.expnext = 100;
        self.growth_attack = 1.11; self.growth_defense = 1.11; self.growth_accuracy = 1.11
        self.growth_evasion = 1.11; self.growth_health = 1.11; self.growth_stamina = 1.11
        
        self.locx = 1; self.locy = 1 #location for drawing
        self.image = 'knight2.png'
        self.sprite = None; self.selected = False #set to true when clicked on and turn is on
        
#return stats
    def get_attack(self): return self.attack
    def get_defense(self): return self.defense
    def get_accuracy(self): return self.accuracy
    def get_evasion(self): return self.evasion
    def get_health(self): return self.health
    def get_stamina(self): return self.stamina
    def get_level(self): return self.level
 #equiping weapons and gaining skills from items, etc
    def equip_weapon(self, weapon):
        self.weapon = weapon
        self.skills.extend(self.weapon.on_equip())
        pass
    
#/////////////Combat procs//////////////////////
  #using a skill  in combat
    def on_attack(self,skill,target):
        skillhits = skill.get_hits()
        i = 0
        while i < skillhits:
            damage = skill.on_use(self,self.weapon)
            totaldamage = target.on_defend(self,damage)
            if totaldamage <= 0: totaldamage = 1
            print self.name+" hits for "+str(totaldamage)
            i += 1
        skill.use_stamina(self,self.weapon)
        return
 #called when a mob is attacked in combat
    def on_defend(self,attacker,damage):
        dfs = self.get_defense()
        atk = attacker.get_attack()
        #todo: code looking for damage type, resistance types, etc, for full defense code later on
        defensemod = float(atk)/float(dfs)
        totaldamage = int(damage*defensemod)
        self.on_damage(totaldamage)
        return totaldamage
    
    def on_damage(self, damage):
        self.health -= damage
        dead = self.death_check()
        if dead == 1: print self.name+" DEADED!"
        
        
    def death_check(self): #returns 1 if mob is dead
        if self.health <= 0:
            self.dead = 1
            return 1
        else: return 0
   
#leveling up and class change procs
    def on_levelup(self):
        self.level += 1; self.expnext = (100+(10*self.level)); self.exp = 0
        print "You level up as a(n) "+self.job+" to level "+str(self.level)
        self.health = int((100*self.level)*self.growth_health)+100
        self.stamina = int((100*self.level)*self.growth_stamina)+100
        self.attack = int((self.level*10)*self.growth_attack)+50
        self.defense = int((self.level*10)*self.growth_defense)+50
        self.accuracy = int((self.level*10)*self.growth_accuracy)+50
        self.evasion = int((self.level*10)*self.growth_evasion)+50
        
        
    def set_stats(self,player): #change characters stats based on player stats
        self.level = player.level
        self.attack = (player.attack*self.growth_attack)
        self.defense = (player.defense*self.growth_defense)
        self.accuracy = (player.accuracy*self.growth_accuracy)
        self.evasion = (player.evasion*self.growth_evasion)
        self.maxhealth = (player.maxhealth*self.growth_health)
        self.maxstamina = (player.maxstamina*self.growth_stamina)
        self.health = self.maxhealth; self.stamina = self.maxstamina #set health and stamina to their full
        
#///////////////////////The Player//////////////////////////
class Player(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.name = "Tim"
        self.job = "Enchanter"
        self.team = 1 #put the player on the players team
        self.growth_attack = 1.22; self.growth_defense = 1; self.growth_accuracy = 1.33
        self.growth_evasion = 1; self.growth_health = 0.89; self.growth_stamina = 1.33
        self.speed = 2
    
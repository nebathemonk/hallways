import random
from mob import Mob
from weapon import *
from skill import *
from combat import * #procedures for combats
from package import * #basic weapons, skills, etc

player = player() #create the player, everything else will follow
player.team = 1

newweapon = sword_short() #create a short sword and equip it
player.equip_weapon(newweapon)

char1 = dummy()
char1.name = "Character one"; char1.team = 1
char2 = dummy() #^ players group members
char2.name = "Character two"; char2.team = 1
enemy1 = dummy()
enemy1.team = 2
enemy2 = dummy()
enemy2.name = "Goblin"; enemy2.team = 2
enemy3 = dummy() #enemy mobs
enemy3.name = "Goblin"; enemy3.team = 2


while True:
    print "1: start combat. l: level up. anything else: quit"
    event = raw_input("select an option:")
    if event == "1":        
        combat(player,char1,char2,enemy1,enemy2,enemy3)

    elif event == "l":
        player.on_levelup()
        print "Health:"+str(player.health)+" Stamina:"+str(player.stamina)
        print "attack:"+str(player.attack)+" defense:"+str(player.defense)
        print "accuracy:"+str(player.accuracy)+" evasion:"+str(player.evasion)
        
    else: break

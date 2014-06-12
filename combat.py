from mob import *
from skill import *
from weapon import *
#from package import *
import operator #for sorting lists

def combat(*args):  
    combatants = [] #all fighters entering combat
    turnlist = [] #used for turnorder, finding targets, etc - only living combatants 
    incombat = True
    for m in args:
        combatants.append(m)
        
    while incombat == True:
        turnlist = get_turnorder(combatants) #get all of the turns, refreshed incase of death
        
        characters = count_side(turnlist,1) #checks to see if one side or the other has been defeated
        enemies = count_side(turnlist,2)
        if enemies < 1:
            print "you win! all enemies defeated."
            break
        if characters < 1:
            print "you lose! all characters defeated"
            break        
        #print turnlist
        for m in turnlist:
            if m.team == 2:
                print "turn for "+m.name+", in turnorder"
                #target = m
            elif m.team == 1:
                attacker = m
                print "turn for "+m.name+", in turnorder"
                if type(m) == player:
                #// get skill > get target > get damage > report damage > continue
                    skill = get_skills(attacker) #player selects skill
                    target = get_target(attacker, skill, turnlist)
                    if target != 1: attacker.on_attack(skill,target)                

def count_side(turnlist,team):
    count = 0
    for m in turnlist:
        if m.team == team: count += 1
    return count
    
def get_target(attacker, skill, chars): #attacking character selects proper number of targets for attacking
    turnlist = chars # build the list of possible targets to choose from
    targets = []
    if skill.type == "offense":
        #print "attacking"
        for m in turnlist:
            if m.team != attacker.team:
                targets.append(m) #add the mob to the target list, is enemy
                #print m.name+" added to targets"
    elif skill.type == "defense":
        for m in turnlist:
            if m.team == attacker.team:
                targets.append(m)
    elif skill.type == "buff":
        targets.append(attacker)
    else: print "What is this? not a skill, that is what."; return 1
    # all possible targets populated in the list, now loop to choose
    choosing = True
    while choosing == True:
        print attacker.name+", choose your target for "+skill.name+":"        
        for index, t in enumerate(targets): #print all of the targets to choose from
            print "["+str(index+1)+"]: "+t.name            
        ch = raw_input("")
        if ch == "1":
            return targets[0]
        elif ch == "2":
            return targets[1]
        elif ch == "3":
            return targets[2] #return the chosen target to mother proc
        elif ch == "4":
            death = raw_input("select the enemy to kill")
            if death == "1": targets[0].dead = 1
            elif death == "2": targets[1].dead = 1
            elif death == "3": targets[2].dead = 1
            return 1    
        else: print "that is not a valid target"
    return 1
    
                
def get_skills(attacker): #player/character selecting attack during turn
    findskill = True
    while findskill == True:
        print attacker.name+" has the following skills using "+attacker.weapon.name+":"        
        for index, s in enumerate(attacker.skills): #print all of the skills to chose from
            print "["+str(index+1)+"]: "+s.name            
        event = raw_input("which skill do you want to use?")        
        if event == "1":        
            #print attacker.name+" uses "+attacker.skills[0].name+" against "+target.name+"!"
            skillsel = attacker.skills[0]
            return skillsel        
        elif event == "2":
            #print attacker.name+" uses "+attacker.skills[1].name+"!"
            skillsel = attacker.skills[1]
            return skillsel
        else: print "invalid selection"
    return 1

def get_turnorder(turnorder): #sort the list of turns
    turns = []
    for m in turnorder:
        if isinstance(m, Mob) == True:
            if m.dead != 1:
                turns.append(m)
        else: print "FUCKS, NOT A MOB"
    turns.sort(key=operator.attrgetter("speed"), reverse=True) #sort combatants by speed, highest first
    return turns
    

from mob import *
from skill import *
from weapon import *
import pygame
from window import *
#from package import *
import operator #for sorting lists

global combatants

def combat(mobs,win):  
    combatants = mobs #all fighters entering combat
    turnlist = [] #used for turnorder, finding targets, etc - only living combatants 
    incombat = True
    win = win
    print "Combated started. All combatants: "+str(combatants)
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
            m.selected = True
            if m.team == 2:
                pygame.time.delay(200)
                print "turn for "+m.name+", in turnorder"
                #target = m
            elif m.team == 1:
                attacker = m
                playerturn(win, combatants, m)
            m.selected = False
                    
        win.refresh(combatants)
                    
def playerturn(win, combatants, attacker):
    print "Player's turn for "+attacker.name+", in turnorder"
    #// get skill > get target > get damage > report damage > continue
    skill = get_skills(win, attacker, combatants) #player selects skill
    print skill
    #target = get_target(attacker, skill, turnlist)
    #if target != 1: attacker.on_attack(skill,target) 
    turn = True
    while turn:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for m in combatants:
                    if m.rect.collidepoint(pygame.mouse.get_pos()):
                        for u in combatants:
                            u.selected = False #unselect all other characters
                        m.selected = True #select the mob so the stat block is updated with their information
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_q]: turn = False
            else: pygame.event.clear()         
        win.refresh(combatants)
    pass
    
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
    
                
def get_skills(win, attacker, combatants): #player/character selecting attack during turn
    print "getting skill"
    findskill = True
    skillicons = []
    for index, s in enumerate(attacker.skills): #print all of the skills to chose from
        print "skill found: "+s.name
        skillx = 230+(34*index)
        skilly = 300
        s.rect = pygame.Rect(skillx,skilly,32,32)
        #print s.rect
        skillimage = pygame.image.load(s.image) 
        skillicon = Icon(skillimage,skillx,skilly)
        win.allgroup.add(skillicon) #create and add the skill icon to be drawn
        skillicons.append(skillicon)
    #win.refresh(combatants)
    while findskill == True: #selecting the skill loop
        #print attacker.name+" has the following skills using "+attacker.weapon.name+":"  
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if s.rect.collidepoint(pygame.mouse.get_pos()): #clicked on a skill
                    return s
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_q]: findskill = False #debug exit loop, will crash shite
                if key[pygame.K_f]: print "Skill loop active, pressed f?"
            else: pass
        win.refresh(combatants)
    for d in skillicons:
        win.allgroup.remove(d)
    del(skillicon)
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
    
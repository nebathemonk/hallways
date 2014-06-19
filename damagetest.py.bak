import random

attack = 340#50 #players attack score
wdamage = 3#2 #weapons damage rating
sdamage = 3#1 #skill damage rating
damage = 0

#damagerange = round(attack*1.5) - round(attack/2) #the difference for number range
damagerange = []
wdamagerange = []
sdamagerange = []

random.seed() #start the number generator

def get_damagerange():
    damagemin = int(attack*0.75)
    damagemax = int(attack*1.5)
    damagecount = damagemin #populate damagerange list
    while damagecount <= damagemax:
        damagerange.append(damagecount)
        damagecount += 1
        
def get_weaponrange():
    if wdamage == 1:
        dmgmn = 0
        dmgmx = int((len(damagerange)*0.33))+1 #bottom third of list
        while dmgmn <= dmgmx:
            wdamagerange.append(damagerange[dmgmn])
            dmgmn += 1
    
    elif wdamage == 2:
        dmgmn = int((len(damagerange)*0.33)) #bottom of list
        dmgmx = int((len(damagerange)*0.66))+1 #top of list, middle third
        while dmgmn <= dmgmx:
            wdamagerange.append(damagerange[dmgmn])
            dmgmn += 1

    elif wdamage == 3:
        dmgmn = int((len(damagerange)*0.66))+1 #bottom of list
        dmgmx = len(damagerange)
        while dmgmn < dmgmx:
            wdamagerange.append(damagerange[dmgmn])
            dmgmn += 1        
    else: pass

def get_skillrange():
    if sdamage == 1:
        dmgmn = 0
        dmgmx = int((len(wdamagerange)*0.33))+1 #bottom third of list
        while dmgmn <= dmgmx:
            sdamagerange.append(wdamagerange[dmgmn])
            dmgmn += 1
    
    elif sdamage == 2:
        dmgmn = int((len(wdamagerange)*0.33)) #bottom of list
        dmgmx = int((len(wdamagerange)*0.66))+1 #top of list, middle third
        while dmgmn <= dmgmx:
            sdamagerange.append(wdamagerange[dmgmn])
            dmgmn += 1

    elif sdamage == 3:
        dmgmn = int((len(wdamagerange)*0.66)) #bottom of list
        dmgmx = len(wdamagerange)
        while dmgmn < dmgmx:
            sdamagerange.append(wdamagerange[dmgmn])
            dmgmn += 1        
    else: pass 

def get_damage():
    damage = int(random.randrange(sdamagerange[0],sdamagerange[-1]))
    return damage
    
get_damagerange()
get_weaponrange()
get_skillrange()
damage = get_damage()

print "damage range of character: ("+str(damagerange)+")"
print "Damage range, with weapon: ("+str(wdamagerange)+")"
print "Damage range, with skill: ("+str(sdamagerange)+")"
print "Total damage (character/weapon/skill random: "+str(damage)


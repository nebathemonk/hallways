from mob import *
from skill import *
from weapon import *
from package import *

player = player() #create the player

print player.name+" has the following skills using "+player.weapon.name+":"
for index, s in enumerate(player.skills):
    print "["+str(index+1)+"]: "+s.name

while True:
    event = raw_input("which skill do you want to use?")
    if event == "1":
        print player.name+" uses "+player.skills[0].name+"!"
        player.on_attack(player.skills[0])
        
    elif event == "2":
        print player.name+" uses "+player.skills[1].name+"!"
        player.on_attack(player.skills[1])
    else: break
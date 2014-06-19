import string
import curses
from map import *
import random
from item import *
from config import *

class MOB(object):
    
    #define a moveable object class
    def __init__ (self,x,y):
        self.health = 100 #set the basic health for a new mob
        self.name = "MOB"
        self.locx = x; self.locy = y #location variables for drawing
        self.icon = "M"; self.color = 1; self.origincolor = 1 #symbol and color pair for drawing
        self.speed = 2; self.turns = 0 #the amount of cycles each turn takes for a player
        self.steps = 0 #the amount of turns taken so far by player
        self.iszombie = 0
        self.inventory = [] #list for inventory items
        
        
    def move(self,event,map): 
        #Movement commands
        if event == "KEY_LEFT":
            colcheck = self.bump(self.locx-1,self.locy,map)
            if colcheck == 1: eventtext = "bump!"
            elif colcheck == 2: eventtext = "Attacked!"
            else:
                self.locx -= 1
                eventtext = self.itemcheck()           
        elif event == "KEY_RIGHT":
            colcheck = self.bump(self.locx+1,self.locy,map)
            if colcheck == 1: eventtext = "bump!"
            elif colcheck == 2: eventtext = "Attacked!"
            else:
                self.locx += 1
                eventtext = self.itemcheck()
        elif event == "KEY_DOWN":
            colcheck = self.bump(self.locx,self.locy+1,map)
            if colcheck == 1: eventtext = "bump!"
            elif colcheck == 2: eventtext = "Attacked!"
            else:
                self.locy += 1
                eventtext = self.itemcheck()
        elif event == "KEY_UP":
            colcheck = self.bump(self.locx,self.locy-1,map)
            if colcheck == 1: eventtext = "bump!"
            elif colcheck == 2: eventtext = "Attacked!"
            else:
                self.locy -= 1
                eventtext = self.itemcheck()
        
        #using/activating items
        elif event == "a":
            item = self.inventory[0]
            eventtext = item.activate(self)            
        #picking up items
        elif event == "g" or event == ",":
            items = []
            for o in itemlist:
                if o.locx == self.locx and o.locy == self.locy: items.append(o)
            if len(items) == 0: eventtext = "There is nothing here to pickup."
            elif len(items) == 1: 
                t = items[0]
                eventtext = "You find a(n) "+t.name+" here and put it in your pack."
                self.inventory.append(t)
                t.held = 1; t.locx = 0; t.locy = 0; itemlist.remove(t)
            elif len(items) > 1: eventtext = self.itempickup(items)
    
        #quick inventory switches
        elif event == "]":
            itemgot = self.inventory[0]
            newlast = self.inventory.pop(0) #get the first item in the list
            self.inventory.append(newlast) #put it at the end of the list
            itemgot = self.inventory[0]
            eventtext = "You look through your pack and grab your "+itemgot.name+"."            
        elif event == "[":
            itemgot = self.inventory[0]
            laspos = len(self.inventory) -1
            newlast = self.inventory.pop(laspos) #get the last item in the list
            self.inventory.insert(0, newlast) #put it at the start of the list
            itemgot = self.inventory[0]
            eventtext = "You look through your pack and grab your "+itemgot.name+"." 
            
        #dropping items
        elif event == "d": #quick drop
            if len(self.inventory) >= 1: #has something in their inventory
                dropitem = self.inventory.pop(0) #drop top item in players inventory
                dropitem.held = 0; dropitem.locx = self.locx; dropitem.locy = self.locy #place on map
                itemlist.append(dropitem)
                eventtext = ("You drop your "+dropitem.name)
            else: eventtext = "You have nothing left to drop!" #player has no items!
            
        elif event == "D": #drop choice menu
            if len(self.inventory) == 1: #only one item, no need for menu
                dropitem = self.inventory.pop(0) #drop top item in players inventory
                dropitem.held = 0; dropitem.locx = self.locx; dropitem.locy = self.locy #place on map
                itemlist.append(dropitem)
                eventtext = ("You drop your "+dropitem.name)
            elif len(self.inventory) > 1: #open the item drop menu
                eventtext = self.itemdrop(self.inventory)
            else: eventtext = "You have nothing left to drop!" #player has no items!
            
        #Debug commands
        elif event == "z": #spawn zombie
            try:
                colcheck = self.bump(self.locx+1,self.locy,map)
                if colcheck != 1:
                    nzombie = MOB((self.locx+1),(self.locy))
                    nzombie.makezombie()
                    moblist.append(nzombie)
                    eventtext = "Zombie spawned!"
                else: eventtext = "Zombie spawn blocked."
            except: eventtext = "NO ZOMBIE FOR YOU"
                
        elif event == "s": #change players speed
            if self.speed == 4: self.speed = 1; eventtext = "COCAINE! (speed = 1)"
            elif self.speed >= 1:
                self.speed += 1
                eventtext = "You slow down a little (speed ="+str(self.speed)+")"
            else: eventtext = "Speed: you shouldn't see this message"
            
        # if any other button not assigned is pressed
        else: eventtext = ("You pressed "+str(event))
        #end and return the eventtext to start loop over        
        return (eventtext)
    
    def itempickup(self,items):
        itemwin = curses.newwin(10,50,17,50)
        itemwin.keypad(1); itemwin.box(); itemwin.bkgd(" ") #make a window to hold items for pickup
        indexselected = []
        itemgot = "you picked up: "
        while True:
            itemwin.addstr(1,1,"PICK UP:")
            for index, i in enumerate(items):
                if i in indexselected:
                    itemwin.addstr(index+2,2,str(index+1)+": "+i.name,curses.A_BOLD) #is selected, bold
                else: itemwin.addstr(index+2,2,str(index+1)+": "+i.name) #not selected, no bold
            event = itemwin.getkey()
            if event == "q": break
            elif event == " ":
                for pickup in indexselected:
                    itemlist.remove(pickup)
                    self.inventory.append(pickup) #pick up all selected items
                    pickup.held = 1; pickup.locx = 0; pickup.locy = 0; #itemlist.remove(pickup)
                    #items.remove(pickup)
                break
            elif event == "1":
                if items[0] in indexselected:
                    indexselected.remove(items[0]) #unselect
                else:
                    indexselected.append(items[0]) #select first option in list
            elif event == "2":
                if items[1] in indexselected:
                    indexselected.remove(items[1]) #unselect
                else:
                    indexselected.append(items[1]) #select first option in list
            elif event == "3":
                if items[2]:
                    if items[2] in indexselected:
                        indexselected.remove(items[2]) #unselect
                    else:
                        indexselected.append(items[2]) #select first option in list
            elif event == "4":
                if items[3]:
                    if items[3] in indexselected:
                        indexselected.remove(items[3]) #unselect
                    else:
                        indexselected.append(items[3]) #select first option in list
            elif event == "5":
                if items[4]:
                    if items[4] in indexselected:
                        indexselected.remove(items[4]) #unselect
                    else:
                        indexselected.append(items[4]) #select first option in list
                    
        itemwin.erase() #clear the window out
        #add items picked up to eventtext
        for index, it in enumerate(indexselected):
            if index == len(indexselected)-1:
                itemgot += it.name+"."
            else:
                itemgot += it.name+", "                
        return itemgot
    
    #/////////////Item Drop/////////////////////////////////
    def itemdrop(self,items):
        itemwin = curses.newwin(10,50,17,50)
        itemwin.keypad(1); itemwin.box(); itemwin.bkgd(" ") #make a window to hold items for pickup
        indexselected = []
        itemdrop = "you put down: "
        while True:
            itemwin.addstr(1,1,"DROP:")
            for index, i in enumerate(items):
                if i in indexselected:
                    itemwin.addstr(index+2,2,str(index+1)+": "+i.name,curses.A_BOLD) #is selected, bold
                else: itemwin.addstr(index+2,2,str(index+1)+": "+i.name) #not selected, no bold
            event = itemwin.getkey()
            if event == "q": break
            elif event == " ":
                for pickup in indexselected:                    
                    self.inventory.remove(pickup) #pick up all selected items
                    pickup.held = 0; pickup.locx = self.locx; pickup.locy = self.locy; #itemlist.remove(pickup)
                    itemlist.append(pickup)
                break
            elif event == "1":
                if items[0] in indexselected:
                    indexselected.remove(items[0]) #unselect
                else:
                    indexselected.append(items[0]) #select first option in list
            elif event == "2":
                if items[1] in indexselected:
                    indexselected.remove(items[1]) #unselect
                else:
                    indexselected.append(items[1]) #select first option in list
            elif event == "3":
                if items[2]:
                    if items[2] in indexselected:
                        indexselected.remove(items[2]) #unselect
                    else:
                        indexselected.append(items[2]) #select first option in list
            elif event == "4":
                if items[3]:
                    if items[3] in indexselected:
                        indexselected.remove(items[3]) #unselect
                    else:
                        indexselected.append(items[3]) #select first option in list
            elif event == "5":
                if items[4]:
                    if items[4] in indexselected:
                        indexselected.remove(items[4]) #unselect
                    else:
                        indexselected.append(items[4]) #select first option in list
                    
        itemwin.erase() #clear the window out
        #add items dropped to eventtext
        for index, it in enumerate(indexselected):
            if index == len(indexselected)-1:
                itemdrop += it.name+"."
            else:
                itemdrop += it.name+", "                
        return itemdrop
    
    def itemcheck(self): #looking for an item on the floor
        itemtext = " "
        items = []
        for o in itemlist:
            if o.locx == self.locx and o.locy == self.locy:
                    items.append(o)
        if len(items) == 1: itemtext = "You see here a(n) "+o.name
        if len(items) > 1:
            itemtext = "items here: "
            for index, i in enumerate(items):
                if index == (len(items)-1): itemtext += i.name+"."
                else: itemtext += i.name+", " #add the item to the list
        return itemtext
    
    def staircheck(self,map): #check players location for stairs
        brow = map.row[self.locy-1] #get the current row to search
        bcol = brow[self.locx-1] #get the column from the row
        if bcol == ">": return 1
        else: return 0
    
    def attackmob(self,target):
        target.color = 7 #change to temp hurt color
        curitem = self.inventory[0]
        target.health -= curitem.damage
        dead = target.deathcheck()
        #atktext = (self.name+" attacks "+target.name+", oh snap!")
        return 
        
    #zombie control functions
    def makezombie(self): #turns a created mob into a zombie
        self.health = 33
        self.icon = "Z"; self.name = "dah zombeh"
        self.color = 4; self.origincolor = 4 #red on black
        self.speed = 3 #two cycles before turn, slower than normal
        self.iszombie = 1
        maul = ITEM("zombie")
        self.inventory = [maul]
        
    def movezombie(self,map):
        if self.turns == self.speed: #the number of cycles passed is equal to their speed, so move
            direction = "s"
            search = self.searchzombie()
            if search != 0:
                if search == 1: direction = "n"
                if search == 2: direction = "s"
                if search == 3: direction = "e"
                if search == 4: direction = "w"
                if search == 5: direction = "ne"
                if search == 6: direction = "nw"
                if search == 7: direction = "se"
                if search == 8: direction = "sw"
            else: direction = random.choice("nwse")
            if direction == "n":
                colcheck = self.bump(self.locx,self.locy-1,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locy -= 1
            elif direction == "s":
                colcheck = self.bump(self.locx,self.locy+1,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locy +=1
            elif direction == "e":
                colcheck = self.bump(self.locx+1,self.locy,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locx +=1
            elif direction == "w":
                colcheck = self.bump(self.locx-1,self.locy,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locx -=1
            elif direction == "se":
                colcheck = self.bump(self.locx+1,self.locy+1,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locy +=1; self.locx +=1
            elif direction == "sw":
                colcheck = self.bump(self.locx-1,self.locy+1,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locy +=1; self.locx -= 1
            elif direction == "ne":
                colcheck = self.bump(self.locx+1,self.locy-1,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locy -=1; self.locx += 1
            elif direction == "nw":
                colcheck = self.bump(self.locx-1,self.locy-1,map)
                if colcheck == 1: zommov = "moved, blocked"+direction; return zommov
                elif colcheck == 2: zommov = "Attacked player!"; return zommov
                else: self.locy +=1; self.locx -= 1
            zommov = "moved"
            self.turns = 0            
        else: self.turns += 1; zommov = "turns = "+str(self.turns)+"."
        return zommov
    
    def searchzombie(self):
        for m in moblist:
            if m.iszombie == 0:
                if m.locx == self.locx - 1 or m.locx == self.locx - 2: return 4 #player to the west
                elif m.locx == self.locx + 1 or m.locx == self.locx + 2: return 3 # to the east
                elif m.locy == self.locy - 1 or m.locy == self.locy - 2: return 1 # to the north
                elif m.locy == self.locy + 1 or m.locy == self.locy + 2: return 2 # to the south
                elif (m.locx == self.locx - 1 or m.locx == self.locx - 2) and (m.locy == self.locy - 1 or m.locy == self.locy - 2):
                    return 6 #north or west
                elif (m.locx == self.locx + 1 or m.locx == self.locx + 2) and (m.locy == self.locy + 1 or m.locy == self.locy + 2):
                    return 7 #south or east
                elif (m.locx == self.locx - 1 or m.locx == self.locx - 2) and (m.locy == self.locy + 1 or m.locy == self.locy + 2):
                    return 5 # north or east
                elif (m.locx == self.locx + 1 or m.locx == self.locx + 2) and (m.locy == self.locy - 1 or m.locy == self.locy - 2):
                    return 8 # south or west
                else: return 0 #player not close enough to attack
            return 0
        return 0
    
 #//////////////////////BUMP BUMP BUMP COMMANDS//////////////////////////////////////////       
    def bump(self,checkx,checky,map):
    #check for border of map
        if checky < 1: return 1
        elif checky > map.maxy: return 1
        elif checkx < 1: return 1
        elif checkx > map.maxx: return 1
    #if border of map fine, look for solid map feature
        brow = map.row[checky-1] #get the current row to search
        bcol = brow[checkx-1] #get the column from the row
        if bcol not in ["."," ",">","<"]: return 1
    #if no feature, check for mob in place
        else:
            for m in moblist:
                if (m.locx == checkx) and (m.locy == checky):
                    self.attackmob(m)
                    return 2
        return 0
    
    def deathcheck(self):
        if self.health <= 0: 
            self.icon = "$"; #mob is dead,
            if self.iszombie == 1:
                corpse = ITEM("corpse")
                corpse.name = "corpse of "+self.name
                corpse.locx = self.locx; corpse.locy = self.locy
                itemlist.append(corpse)
                dindex = moblist.index(self)
                deadmob = moblist.pop(dindex)
                mobdead.append(deadmob) #move mob to the list of dead mobs
            return 1
        else: return 0
     
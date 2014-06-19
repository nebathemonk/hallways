import curses
import curses.panel
import curses.wrapper
import string

from random import randrange
from operator import attrgetter

from mob import * 
from map import *
from item import *
from config import *


screen = curses.initscr()
curses.start_color()

curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK) #white normal, map color
curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_BLUE) #stat panel background
curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_BLACK) #ranger
curses.init_pair(4,curses.COLOR_RED,curses.COLOR_BLACK) #zombie color, medkit
curses.init_pair(5,curses.COLOR_MAGENTA,curses.COLOR_BLACK) #ranged weapon
curses.init_pair(6,curses.COLOR_CYAN,curses.COLOR_BLACK) #melee weapon
curses.init_pair(7,curses.COLOR_BLACK,curses.COLOR_RED) #zombie hurt color
curses.init_pair(8,curses.COLOR_YELLOW,curses.COLOR_BLUE) #half heath
curses.init_pair(9,curses.COLOR_RED,curses.COLOR_BLUE) # 1/3 health

curses.use_default_colors()

map = MAP(maplevel) #create a new map

win = curses.newwin(40,150,0,0)
win2 = win.derwin(5,150,0,0)
win3 = win.derwin(35,30,5,120)
win4 = win.derwin((map.maxy+2),(map.maxx+2),(17-(map.maxy/2)),(60-(map.maxx/2)))

player = MOB(map.starty,map.startx) #create a new player
zombie = MOB(6,8) #make a zombie

chainsaw = ITEM("chainsaw"); medkit = ITEM("medkit"); handgun = ITEM("handgun")
chainsaw.selected = 1; chainsaw.held = 1; medkit.held = 1
handgun.locx = 5; handgun.locy = 6; #set the handgun starting location

itemlist.append(handgun)
moblist.append(player)
moblist.append(zombie)
#moblist = [player,zombie] #population list

def main():
    
    curses.noecho() #takes of echo but allows key input
    curses.cbreak() #enables no need to wait for enter key for input
    curses.curs_set(0)
    win.keypad(1) #adds special keys     
    
    win2.bkgd(" ",curses.color_pair(2)) #game log
    win2.box()    
    
    win3.bkgd(" ",curses.color_pair(2)) #stat/information panel
    win3.box()
 
    win4.bkgd(" ",curses.color_pair(1)) #the map area
    win4.box() 
    zombie.makezombie()
    player.color = 3; player.origincolor = 3; player.name = "Player"; player.icon = "@"
    player.inventory = [chainsaw,medkit]
    
    gameloop(map,maplevel) #start the game control loop
 
def refresh():    
    win.erase() #clear the whole screen and redraw each window
         
    win2.bkgd(" ",curses.color_pair(2))
    win2.box()       
    win3.bkgd(" ",curses.color_pair(2))
    win3.box()
    win4 = win.derwin((map.maxy+2),(map.maxx+2),(17-(map.maxy/2)),(60-(map.maxx/2)))
    #win4.mvderwin((17-(map.maxy/2)),(60-(map.maxx/2)))
    win4.bkgd(" ",curses.color_pair(1))
    map.draw(win4,1,1)
    win4.box()
    map.drawitems(win4)
    for m in moblist:
        win4.addch(m.locy,m.locx,ord(m.icon), curses.color_pair(m.color))
    statblock()
    for m in moblist:
        m.color = m.origincolor #set all damaged mobs back to original color
    
 
    
def statblock():
    win3.addstr(1,2,str(player.icon),curses.color_pair(player.color))
    if player.health >= 67: win3.addstr(1,3,": Health:"+str(player.health))
    elif player.health >= 34: win3.addstr(1,3,": Health:"+str(player.health),curses.color_pair(8))
    elif player.health < 34: win3.addstr(1,3,": Health:"+str(player.health),curses.color_pair(9))
    win3.addstr(2,3,"Turns: "+str(player.steps))
    win3.addstr(3,2,"Loc: ("+str(player.locx)+","+str(player.locy)+") Lvl: "+str(maplevel))
    drawinv()

def drawinv():
    sorted(player.inventory, key=attrgetter('selected'), reverse=True)
    itemnum = 0
    for item in player.inventory:
        itemnum += 1
        if itemnum == 1:
            win3.addch(2+(itemnum*2),1,ord(item.icon),curses.color_pair(item.color))
            win3.addstr(2+(itemnum*2),2,": "+str(item.name),curses.A_BOLD)
            win3.addstr(3+(itemnum*2),3,"Dmg: "+str(item.damage_rating)+"  Range: "+str(item.range_rating),curses.A_BOLD)
        else:
            win3.addch(2+(itemnum*2),1,ord(item.icon),curses.color_pair(item.color))
            win3.addstr(2+(itemnum*2),2,str(item.name)+":")
            win3.addstr(3+(itemnum*2),3,"Dmg: "+str(item.damage_rating)+"  Range: "+str(item.range_rating))
    
def gameloop(map,maplevel):
    refresh()
    win.addstr(1,1,"Hit any button to begin the game.")
    win.addstr(2,1,"q: exits. Arrows move. i: inventory")
    win.addstr(3,1,"z: spawns zombie g: picks up item d: drops item")

    while True:
        event = win.getkey()              
        if event == "q":
            break #wait for input and then close
        #inventory - cycle loop
        elif event == "i": 
            itemgot = inventoryloop()
            eventtext = ("You look through your bag and grab your "+itemgot+".")
        #Stairs up or down
        elif event == ">":
            stairs = player.staircheck(map)
            if stairs == 1:
                eventtext = "You go down the stairs."
                changemap(win,maplevel)
                player.locx = map.startx; player.locy = map.starty #position the player at map start
            #this is where the 'go to next level' should be
            else: eventtext = "You see no stairs to go down here..."
        else: eventtext = player.move(event, map)
        player.steps += 1
        player.turns = 0
        turnstaken = 0
        while player.turns < player.speed: #run a number of cycles based on pc speed
            for m in moblist: 
                if m.iszombie == 1: zommov = m.movezombie(map)  
            player.turns += 1
            turnstaken += 1
        if eventtext != " ": log.insert(0,eventtext)
        if len(log) > 3: oldtext = log.pop(len(log)-1)
        refresh()
        for index, text in enumerate(log):
            win2.addstr(3-index,1,text)
        
def changemap(win,maplevel):
    for i in itemlist: itemlist.remove(i)
    for m in moblist:
        if m.iszombie == 1: moblist.remove(m)
    maplevel += 1
    map.buildmap(maplevel)
    #change the map!
    
#////////////////////////Inventory Loop///////////////////////////
def inventoryloop():
        itemgot = player.inventory[0]
        while True:
            event = win.getkey()
            if event == "q": break
            elif event == " ": break
            elif event == "KEY_DOWN":
                newlast = player.inventory.pop(0) #get the first item in the list
                player.inventory.append(newlast) #put it at the end of the list
                itemgot = player.inventory[0]
                refresh() #redraw the screen                   
            elif event == "KEY_UP":
                laspos = len(player.inventory) -1
                newlast = player.inventory.pop(laspos) #get the last item in the list
                player.inventory.insert(0, newlast) #put it at the start of the list
                itemgot = player.inventory[0]
                refresh() #redraw the screen
            elif event == "KEY_RIGHT": break
            elif event == "KEY_LEFT": break 
            else: itemgot = itemgot 
        return itemgot.name
if __name__ == "__main__":
    curses.wrapper(main())

win.keypad(0); curses.nocbreak();  curses.echo() #undo all the editting so the terminal works right
curses.endwin()





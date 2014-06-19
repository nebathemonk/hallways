from map import *
import curses
import string
#import map
from mob import * 
from item import *

#////////////////////////GLOBAL VARIABLES/////////////////////////
maplevel = 1 #the level, used for map file opening
itemlist = [] #list of all of the items sitting around
moblist = [] #list of mobs living in world
#the current map created
mobdead = [] #list of mobs that have died
log = []#list of strings from eventtexts, used for history
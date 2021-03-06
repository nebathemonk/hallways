import random
import sys
from mob import Mob
from weapon import *
from skill import *
from combat import * #procedures for combats
from package import * #basic weapons, skills, etc
from window import *
import pygame

if len(sys.argv) > 1:
    print "yes, massa, creating window of "+sys.argv[1]+"x"+sys.argv[2]
    width = int(sys.argv[1]); height = int(sys.argv[2]) #if there are commandline args, use them to set the width and height
else: 
    width = 640; height = 480 #else, default to 640, 480
    
win = Window(width,height,"bkg.png")
characters = []
#playerloc = (1,1)
char1loc = (120,110)
char2loc = (1,200)
enemy1loc = (500,0)
enemy2loc = (430,100)
enemy3loc = (500,220)

player = Player()
player.rect = pygame.Rect(player.locx, player.locy, 96, 128) #create a collision box around player icon
player.selected = True #turn starts with the first player so far

newweapon = sword_short() #create a short sword and equip it to the player for skilllls
player.equip_weapon(newweapon)

char1 = Bob()
char1.locx, char1.locy = char1loc
char1.rect = pygame.Rect(char1.locx, char1.locy, 96, 128)

char2 = Sarah()
char2.locx, char2.locy = char2loc
char2.rect = pygame.Rect(char2.locx, char2.locy, 96, 128)

enemy1 = Goblin()
enemy1.locx, enemy1.locy = enemy1loc
enemy1.rect = pygame.Rect(enemy1.locx, enemy1.locy, 60, 96)

enemy2 = Goblin()
enemy2.locx, enemy2.locy = enemy2loc
enemy2.rect = pygame.Rect(enemy2.locx, enemy2.locy, 60, 96)

enemy3 = Goblin()
enemy3.locx, enemy3.locy = enemy3loc
enemy3.rect = pygame.Rect(enemy3.locx, enemy3.locy, 60, 96)

characters = [player, char1, char2, enemy1, enemy2, enemy3] #list of all the characters active in the game

win.loadimages(characters) #preload all of the images needed for characters

running = 1
while running == 1: #game loop start
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for m in characters:
                if m.rect.collidepoint(pygame.mouse.get_pos()):
                    for u in characters:
                        u.selected = False #unselect all other characters
                    m.selected = True #select the mob so the stat block is updated with their information
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_c]: combat(characters, win)
            elif key[pygame.K_q]: running = 0
        if event.type == pygame.QUIT: running = 0
        else: pygame.event.clear()         
            
    win.refresh(characters)

pygame.quit() #game loop is over, close the window
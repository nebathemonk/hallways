import sys #commandline reading 
import pygame
from pygame.locals import *
import random

if len(sys.argv) > 1:
    print "yes, massa, creating window of "+sys.argv[1]+"x"+sys.argv[2]
    width = int(sys.argv[1]); height = int(sys.argv[2]) #if there are commandline args, use them to set the width and height
else: 
    width = 640; height = 480 #else, default to 640, 480

pygame.init()
screen = pygame.display.set_mode((width,height)) #create the screen (640 wide, 480 tall by default)
clock = pygame.time.Clock()

#/////////COLOR DEFINITIONS
blue = 0,0,255 #blue, defined by rbg scale
black = 0,0,0
gray = 15,15,15
red = 255,0,0
green = 0,255,0
purple = 150, 0, 150
yellow = 200,225,0
mystery = ((random.randint(0,255)),(random.randint(0,255)),(random.randint(0,255))) #random values for mystery color!

colors = [blue,black,gray,red,green,purple,yellow,mystery] #a list of all defined colors, for randomly picking them.

pygame.mouse.set_visible(False)
running = 1 #start the game loop running
LEFT = 1 #the left mouse button, for click events

text = pygame.font.Font('freesansbold.ttf',14)
textsurface = text.render("This is text? Fuck.",True,green) #create a surface with the text

horizon = (height / 2)
vertical = (width / 2)
#for making tiles?
tilesx = int(width/32)
tilesy = int(height/32)

tl = 0,0; tr = width-1,0; bl = 0,height-1; br = width-1,height-1 #top, bottom, left, right of main screen (at 640x480)
hl = 0,horizon; hr = width-1,horizon
vt = vertical,0; vb = vertical, height-1


barcolor = []
barheight = 32
for i in range(1,63):
    barcolor.append((0,0,i*6)) #increase blue steps
for i in range(1,63):
    barcolor.append((0,0,255 - i*4))
    
barstart = int((width*0.33)); barend = (int(width*0.66)) #put the bar in the middle third of the screen


y = 0; dir = 2 #for scanning/moving line
x = (width/2); xdir = 1
cursorx = 0; cursory = 0 #used to draw the cursor lines
curcolor = black
#//////////////cartesian coordinations
#origin = (width/2), (height/2) #create a tuple of the center point of the screen

def explosion(pos): #draw a circle where the mouse is pressed
    x, y = pos
    e = 2
    while e < 25:
        pygame.draw.circle(screen,curcolor,(x,y),e)
        e += 1
        pygame.display.flip()
    return

while running: #main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0 #wait for quit command, then end program
        if event.type == pygame.MOUSEMOTION:
            cursorx, cursory = event.pos
            cartx = 0; carty = 0
            if event.pos[0] > vertical: cartx = (event.pos[0]-vertical)
            elif event.pos[0] <= vertical: cartx = (event.pos[0]-vertical)
            if event.pos[1] > horizon: carty = (event.pos[1]-horizon)
            elif event.pos[1] <= horizon: carty = (event.pos[1]-horizon)
        #print "mouse at (%d, %d)" %(cartx, carty)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            print "you pressed the mouse button at (%d, %d)" %(cartx, carty)
            explosion(event.pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            print "you left up the mouse button at (%d, %d)" %(cartx, carty)
            explosion(event.pos)
        #else: print event.type
    
    #bkgcolor = colors[random.randrange(0,(len(colors)-1))]
    #bkgcolor = colors[-1]
    screen.fill(black) #fill with black
    
    #draw tile lines
    t = 0
    while t < tilesx:
        pygame.draw.line(screen,gray,(32*t,0),(32*t,height))
        pygame.draw.line(screen,gray,(0,32*t),(width,32*t))
        t += 1
        
    #draw cross lines
    pygame.draw.line(screen, blue, tl, br)
    pygame.draw.line(screen, blue, tr, bl)
    pygame.draw.line(screen, red, hl, hr) #horizontal line
    pygame.draw.line(screen, red, vt, vb) #vertical line
    pygame.draw.circle(screen, red, (vertical,horizon), 3) #draw a dot at the cartesian center point
    
    #draw that funky shape!
    climbx = 0; climby = height
    while climbx < width:
        pygame.draw.line(screen, green, (0,climby), (climbx,0))
        #pygame.draw.line(screen, green, )
        climbx += (width/20) #add 1/20 screen width and draw again
        climby -= (height/20)
    
    #moving line?
    pygame.draw.line(screen, purple, (0,y), (width,y))
    pygame.draw.line(screen, purple, (x,0), (x,height))
    y += dir; x += xdir
    if y <= 0 or y >= height: dir *= -1 #hit the edge, flip direction
    if x == 0 or x == width: xdir *= -1
    
    #draw cross bars to mouse cursor:
    if cartx > 0 and carty > 0: curcolor = red
    elif cartx > 0 and carty <= 0: curcolor = green
    elif cartx <= 0 and carty > 0: curcolor = blue
    elif cartx <= 0 and carty <= 0: curcolor = yellow
    else: curcolor = black
    pygame.draw.line(screen, curcolor, (cursorx-5,cursory),(cursorx+5,cursory))
    pygame.draw.line(screen, curcolor, (cursorx,cursory-5), (cursorx, cursory+5))
    
    #draw the gradient bar
    for i in range (0, barheight):
        pygame.draw.line(screen, barcolor[i], (barstart,height-i),(barend,height-i))
        
    #Draw text over the gradient bar
    curtext = "(%d, %d)" %(cartx, carty)
    textsurface = text.render(curtext,True,curcolor)
    screen.blit(textsurface,(cursorx,cursory))
    
    pygame.display.flip() #update screen
    clock.tick(48)
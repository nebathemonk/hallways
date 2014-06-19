import curses
from item import *
from config import *
from mob import *



class MAP(object):    
 
    def buildmap(self,level): 
        if level == 1: self.maxx = 19; self.maxy = 10; self.startx = 1; self.starty = 1
        elif level == 2: self.maxx = 30; self.maxy = 22; self.startx = 2; self.starty = 11
        mapfile = open('level'+str(level)+'.map','r') #open the file specified by level var
        
        line = 0
        for cols in mapfile.readlines():
            try:
                self.row[line] = cols
                line += 1
            except:
                maperr = "failure reading lvl "+str(level)+" row "+str(line)+" col "+str(cols)
                errwin = newwin(10,50,40,60) #make an error window
                errwin.addstr(1,1,"MAP READ ERROR")
                errwin.addstr(2,1,newmap)
                ok = errwin.getch()
                errwin.erase()
        mapfile.close()
        return 
     
    def __init__ (self,level):
        self.maxx = 0; self.maxy = 0; self.startx = 1; self.starty = 1
        self.a = [];self.b = [];self.c = [];self.d = [];self.e = [] #row lists, each index is a column
        self.f = [];self.g = [];self.h = [];self.i = [];self.j = []
        self.k = [];self.l = [];self.m = [];self.n = [];self.o = []
        self.p = [];self.q = [];self.r = [];self.s = [];self.t = []
        self.u = [];self.v = [];self.w = [];self.x = [];self.y = []; self.z = [] 
        self.row = [self.a,self.b,self.c,self.d,self.e,self.f,self.g,self.h,self.i,self.j,
            self.k,self.l,self.m,self.n,self.o,self.p,self.q,self.r,self.s,self.t,self.u,self.v,
            self.w,self.x,self.y,self.z] #add all the rows to the map
        self.buildmap(level)
            
        
        
        
        
    def draw(self,win,x,y):
        originx = x
        for r in self.row:
            for i in r:
                try:
                    drawch = ord(i)
                    win.addch(y,x,drawch) #print a piece of the map
                    x += 1
                except: win.addstr(0,0,"failure at: "+str(x)+","+str(y))
            x = originx
            y += 1
        return 
    
    def drawitems(self,win):
        for o in itemlist:
            drawitem = ord(o.icon)
            win.addch(o.locy,o.locx,drawitem,curses.color_pair(o.color))
        return 
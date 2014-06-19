import pygame

WHITE = (255,255,255) #color definitions
BLACK = (0,0,0)

class Icon(pygame.sprite.DirtySprite):
    def __init__(self,image,x,y):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y
        
        
class Window(object):
    def __init__(self,width, height, background):    
        pygame.init()
        self.screen = pygame.display.set_mode((width,height)) #create the screen (640 wide, 480 tall by default)
        self.clock = pygame.time.Clock()
        self.screen.fill((0,0,0))
        self.background = pygame.image.load(background)
        #self.icondict = {} #dictionary type?!
        self.allgroup = pygame.sprite.LayeredUpdates()#holds all the sprites        
        
        self.text = pygame.font.Font('freesansbold.ttf',14) #create a text object for displaying text
        
        self.highlight = pygame.image.load('highlight.png') #create a highlighter
        self.hlicon = Icon(self.highlight,0,0)
        self.hlicon.visible = 0 #make the highlighter invisible at first
    
    def refresh(self,characters): #redraw all the characters and refresh the screen
        self.screen.blit(self.background,(0,0))        
        self.allgroup.clear(self.screen,self.background)
        self.allgroup.draw(self.screen)
        
        for m in characters:
            if m.rect.collidepoint(pygame.mouse.get_pos()):
                chartext = "%s: level %d" %(m.name, m.level)
                charname = self.text.render(chartext,True,WHITE,BLACK) #create text
                self.screen.blit(charname,(m.locx,m.locy)) #display text at character
            if m.selected == True:
                self.highlight_mob(m) #draw m's stats because they are selected
        pygame.display.flip()
        
        
    def loadimages(self,characters):
        self.allgroup.add(self.hlicon) #add the highlighter to bottom layer
        for m in characters:
            preimage = pygame.image.load(m.image)
            newicon = Icon(preimage,m.locx,m.locy)
            m.sprite = newicon
            self.allgroup.add(newicon) #add the player icons above that
    
    def highlight_mob(self,character): #when selected
        self.hlicon.visible = 1 #make sure the highlighter is visible
        self.hlicon.rect.topleft = (character.locx, character.locy) #highlighter icon
        #statblock texts
        statline1 = self.text.render((character.name+": "+str(character.level)),True,BLACK)
        statline2 = self.text.render(("Health: "+str(character.health)+"/"+str(character.maxhealth)),True,BLACK)
        statline3 = self.text.render(("Stamina: "+str(character.stamina)+"/"+str(character.maxstamina)),True,BLACK)
        self.screen.blit(statline1,(20,350))
        self.screen.blit(statline2,(20,370))
        self.screen.blit(statline3,(20,390))
        
    
            
            
            
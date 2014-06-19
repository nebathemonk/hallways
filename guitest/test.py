import pygame
import string
from mob import *
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self._image_surf = None 
        self._image_surf = None
        player.locx = 20; player.locy = 200
        #self.imagex = 20; self.imagey = 200
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._image_surf = pygame.image.load("/home/neba/projects/guitest/bkgrd.png").convert()
        self._image_surf2 = pygame.image.load("/home/neba/projects/guitest/hero.png").convert_alpha()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            keypressed = pygame.key.get_pressed()
            if keypressed[K_LEFT]:
                player.locx -= 1
            if keypressed[K_RIGHT]:
                player.locx += 1
            if keypressed[K_q]:
                self._running = False
            
    def on_loop(self):
        pygame.display.flip()
        timer.tick(40)
        pygame.display.set_caption("fps: "+ str(timer.get_fps()))
        pass
    
    def on_render(self):
        ext = pygame.image.get_extended()
        if ext == True:
            self._display_surf.blit(self._image_surf,(0,0))
            self._display_surf.blit(self._image_surf2,(player.locx,player.locy))     
        pass
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            event = pygame.event.poll()
            self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    timer = pygame.time.Clock()
    player = Mob()
    theApp = App()
    theApp.on_execute()


import pygame
from pygame.locals import *
 
class NPC:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 840, 600
        self.background=255,255,255


    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        ## load npc
        self.npc_minion = pygame.image.load("../pic/npc_minion.jpeg")
        self.npc_minion_rect = self.npc_minion.get_rect()
        self.speed=[2,0]
        self.npc_minion_rect.x=500
        self.npc_minion_rect.y=200
        #self.npc_minion_rect.size=
    def on_event(self, event):

        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        '''
        self.npc_minion_rect = self.npc_minion_rect.move(self.speed)
        if self.npc_minion_rect.left < 0 or self.npc_minion_rect.right > self.width:
            self.speed[0] = -self.speed[0]
        if self.npc_minion_rect.top < 0 or self.npc_minion_rect.bottom > self.height:
            self.speed[1] = -self.speed[1]
        '''
        #pass

    def on_render(self):
        self.screen.fill(self.background)
        self.screen.blit(self.npc_minion, self.npc_minion_rect)
        pygame.display.flip()
        #pass

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theNPC = NPC()
    theNPC.on_execute()
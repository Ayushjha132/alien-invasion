import sys
import pygame

from settings import Settings 
from ship import Ship


class AlienInvasion:
    
    def __init__(self):

        #initialize pygame 
        pygame.init()

        #to control the fps
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #setup screen for the game
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption("Alien Invasion")

        #instance of ship class
        self.ship = Ship(self)
    
    
    # the gae willl be controlled by run_game method.
    def run_game(self):
        
        while True:
            
            self._check_events()
            #update the ship position 
            self.ship.update()
            self._update_screen()
            
            #60 fps 
            self.clock.tick(60)

    def _check_events(self):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        self._check_keydown_events(event)

                    elif event.type == pygame.KEYUP:
                        self._check_keyup_events(event)
                        
                        
    # response to key presses        
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #quit with press 'q'
        elif event.key == pygame.K_q:
            sys.exit()
    
    #response to key releases   
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):

        #setting color of screen contain in setting through each loop
        self.screen.fill(self.settings.bg_color)

        #placeing on screen
        self.ship.blitme()
                
        #bring the pygame tab in the front
        pygame.display.flip()



if __name__ == '__main__':

    # a game instance, and run the game. 

    ai = AlienInvasion()
    ai.run_game()

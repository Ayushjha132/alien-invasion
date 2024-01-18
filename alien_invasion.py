import sys
import pygame

from settings import Settings 
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    
    def __init__(self):

        #initialize pygame 
        pygame.init()

        #to control the fps
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #setup screen for the game
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # with the screen the "q" Quit not work. 
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        #instance of ship class
        self.ship = Ship(self)
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._creat_fleet()
    
    
    # the gae willl be controlled by run_game method.
    def run_game(self):
        
        while True:
            
            self._check_events()
            #update the ship position 
            self.ship.update()
            self.bullets.update()
            self._update_bullets()
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    #response to key releases   
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    #create a bullet and add to the goup of bullets.
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
    
    #create fleet of aliens
    def _creat_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width


        current_x = alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width
    
    def _update_screen(self):

        #setting color of screen contain in setting through each loop
        self.screen.fill(self.settings.bg_color)

        """ sprites() return the list that this group contains"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #placeing on screen
        self.ship.blitme()

        self.aliens.draw(self.screen)
                
        #bring the pygame tab in the front
        pygame.display.flip()



if __name__ == '__main__':

    # a game instance, and run the game. 

    ai = AlienInvasion()
    ai.run_game()

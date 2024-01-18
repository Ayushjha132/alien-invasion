import sys
import pygame
from time import sleep

from settings import Settings 
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

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

        #insatnce of game_stats
        self.stats = GameStats(self)

        #instance of ship class
        self.ship = Ship(self)
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

        #start game in inactive state
        self.game_active = False

        #button instance
        self.play_button = Button(self, "Play")
    
    
    # the gae willl be controlled by run_game method.
    def run_game(self):
        
        while True:
            
            self._check_events()

            if self.game_active:
                #update the ship position 
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            
            self.stats.reset_stats()
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()
            #hide the cursor while game active
            pygame.mouse.set_visible(False)


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
                
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        #pygame deletes when two agruments pairs returns true. 
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        """ groupcollide() stores the key value pairs to the dictionary."""

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    
    #create fleet of aliens
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # to restart from the one space alien width from hotizontal side
            current_x = alien_width
            # adding row space 
            current_y += 2 * alien_height

    
    #creating a alien and placing in the row
    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

        """when alien touch the bottom will be treated as ship hit"""
    def _check_alien_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        #ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()

        #alien reach the bottom
        self._check_alien_bottom()


    
    def _update_screen(self):

        #setting color of screen contain in setting through each loop
        self.screen.fill(self.settings.bg_color)

        """ sprites() return the list that this group contains"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #placeing on screen
        self.ship.blitme()

        self.aliens.draw(self.screen)

        #draw button in inactive state
        if not self.game_active:
            self.play_button.draw_button()
                
        #bring the pygame tab in the front
        pygame.display.flip()




if __name__ == '__main__':

    # a game instance, and run the game. 

    ai = AlienInvasion()
    ai.run_game()


# contains all the settings of game
class Settings:
    
    def __init__(self):

        #screeen settings
        self.screen_width = 1280
        self.screen_height = 700 
        self.bg_color = (230, 230, 230) 

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3
        
        #bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #aliens settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # -1 left and 1 right directions
        self.fleet_direction = 1





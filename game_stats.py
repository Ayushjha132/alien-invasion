class GameStats:
    def __init__(self, ai_game):
        self.setttings = ai_game.settings
        self.reset_stats()
        self.high_score = 0
    
    def reset_stats(self):
        self.ships_left = self.setttings.ship_limit
        self.score = 0
        self.level = 1
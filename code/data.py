class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0
        self._health = 5
        self.ui.create_hearts(self._health)

        self.unlocked_level = 1
        self.current_level = 0

    # Decorators, a getter and a setter
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)

    @property
    def coins(self):
        return self._coins
    
    @coins.setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.coins)
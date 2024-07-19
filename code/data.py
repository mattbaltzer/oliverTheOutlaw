class Data:
    def __init__(self, ui):
        self.ui = ui
        self.coins = 0
        self._health = 5

    # Decorators, a getter and a setter
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
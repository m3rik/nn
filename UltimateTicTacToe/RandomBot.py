from Bot import Bot
from State import Move, State

import random

class RandomBot(Bot):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def move(self, state, symbol):
        while True:
            x,y = random.randint(0, 8),random.randint(0, 8)
            if state.get_board()[y,x] == 0 and not state.is_finished_minigame(int(x / 3), int(y / 3)):
                break
        return Move(x,y)
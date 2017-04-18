class Bot:
    '''
        state - state of the game
        returns a move
    '''
    def move(self, state, symbol):
        raise NotImplementedError('Abstractaaa')

    def get_name(self):
        raise NotImplementedError('Abstractaaa')

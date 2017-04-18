import numpy as np

class State:
    def __init__(self):
        self.board = np.zeros((9,9), dtype=np.int32)
        self.game = np.zeros((3,3), dtype=np.int32)


    def clone(self):
        s = State()
        s.board = np.array(self.board)
        return s

    '''
        use this to get the board
    '''
    def get_board(self):
        return self.board

    def print_board(self):
        print('=' * 21)
        for i in range(9):
            for j in range(9):
                if self.board[i,j] == 0:
                    print('.',)
                elif self.board[i,j] == 1:
                    print('X',)
                else:
                    print('O',)

                if (j + 1) % 3 == 0:
                    print(' ',)
            print()
            if (i + 1) % 3 == 0:
                print()
        print('=' * 21)

        self.is_finished()

        print('=' * 5)
        for i in range(3):
            for j in range(3):
                if self.game[i,j] == 0:
                    print('.',)
                elif self.game[i,j] == 1:
                    print('X',)
                else:
                    print('O',)
            print()
        print('=' * 5)




    '''
        helper function
    '''
    def _is_finished_minigame(self, minigame):
        for i in range(0, 3):
            is_finished = True
            if minigame[i,0] == 0:
                continue
            for j in range(1, 3):
                if minigame[i,j] != minigame[i,0]:
                    is_finished = False
            if is_finished:
                return minigame[i,0]
        for j in range(0, 3):
            is_finished = True
            if minigame[0,j] == 0:
                continue
            for i in range(1, 3):
                if minigame[i,j] != minigame[0, j]:
                    is_finished = False
            if is_finished:
                return minigame[0,j]
        is_finished = (minigame[0,0] == minigame[1,1]) and (minigame[0,0] == minigame[2,2] and minigame[1,1] != 0)
        if is_finished:
                return minigame[1,1]
        is_finished = (minigame[2,0] == minigame[1,1]) and (minigame[1,1] == minigame[0,2] and minigame[1,1] != 0)
        if is_finished:
                return minigame[1,1]
        if np.count_nonzero(minigame) == 9:
            return 0

        return None

    '''
        Returns None is the game is not finished
        otherwise returns the result of the match
        1 or -1 if one of the player wins
        0 if it's a draw
    '''
    def is_finished_minigame(self, x, y):
        i,j = y, x
        minigame = self.board[i*3:(i+1)*3, j*3:(j+1)*3]
        result = self._is_finished_minigame(minigame)
        return result

    '''
        returns True or False
    '''
    def is_finished(self):
        hasRemainingMatches = False
        for i in range (0,3):
            for j in range(0,3):
                minigame = self.board[i*3:(i+1)*3, j*3:(j+1)*3]
                result = self._is_finished_minigame(minigame)
                if (result == None):
                    hasRemainingMatches = True
                    self.game[i,j] = 0
                else:
                    self.game[i,j] = result
        result = self._is_finished_minigame(self.game)
        if result != None:
            return True
        if hasRemainingMatches:
            return False
        return True

    '''
        decides the winner
    '''
    def winner(self):
        if self.is_finished():
            return self._is_finished_minigame(self.game)
        return None

    def is_valid(self, move, symbol):
        if move.posx < 0 or move.posx > 8 or move.posy < 0  or move.posy > 8:
            raise Exception('Invalid move. Position out of range.')
        if self.board[move.posy, move.posx] != 0:
            raise Exception('Invalid move. There is an existing piece already.')

        idx = int(move.posx / 3)
        idy = int(move.posy / 3)
        if self.is_finished_minigame(idx, idy) != None:
            raise Exception('Invalid move. This minigame is already over')

        self.board[move.posy, move.posx] = symbol

class Move:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy





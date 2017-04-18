from State import State
from Bot import Bot
import traceback
import sys
import time
from TimeoutDecorator import timeout

class GameEngine:
    def __init__(self, bot1, bot2):
        self.bot1 = bot1
        self.bot2 = bot2

    def get_symbol(self, value):
        if value == 1:
            return 'X'
        return 'O'

    def _play_n_games(self, N, verbose=True, verboseExceptions=False, init_state=State(), init_symbol=1):
        countDraws = 0
        countBot1 = 0
        countBot2 = 0

        for i in range(N):

            start = time.time()
            result = self.play(init_state=init_state.clone(),init_symbol=init_symbol)
            end = time.time()
            if result == self.bot1:
                countBot1 += 1
                if verbose:
                    print(self.bot1.get_name() + ' won!')
            elif result == self.bot2:
                countBot2 += 1
                if verbose:
                    print(self.bot2.get_name() + ' won!')
            else:
                countDraws += 1
                if verbose:
                    print('Draw!')
            if verbose:
                print('Game finished in: ' + str(end - start))

        return countBot1, countBot2, countDraws

    def play_n_games(self, N, verbose=True, verboseExceptions=False, init_state=State(), init_symbol=1):
        if verbose:
            print('Started to play ' + str(N) + ' games between ' + self.bot1.get_name() + ' and ' + self.bot2.get_name())
        cb1, cb2, cd = self._play_n_games(int(round(N/2)), verbose=verbose, verboseExceptions=verboseExceptions,init_state=init_state.clone(), init_symbol=init_symbol)
        self.bot1, self.bot2 = self.bot2, self.bot1
        cb2t, cb1t, cdt = self._play_n_games(int(round(N/2)), verbose=verbose, init_state=init_state.clone(), init_symbol=init_symbol)
        cb1 += cb1t
        cb2 += cb2t
        cd += cdt
        if verbose:
            print()
        return cb1, cb2, cdt

    @timeout(2)
    def get_bot_move(self, bot, state, sym):
        return bot.move(state, sym)


    """
        returns the winning bot
    """
    def play(self, verbose=False, verboseExceptions=True, delay=0, init_state=State(),init_symbol=1):
        symbols = [init_symbol, -init_symbol]
        bots = [self.bot1, self.bot2]
        cur_symbol = 0

        new_state = init_state

        if verbose:
            new_state.print_board()

        dict = {}
        dict[symbols[0]] = self.bot1
        dict[symbols[1]] = self.bot2

        while not new_state.is_finished():
            sym = symbols[cur_symbol]
            try:
                #move = bots[cur_symbol].move(new_state.clone(), sym)
                move = self.get_bot_move(bots[cur_symbol], new_state.clone(), sym)
                if verbose:
                    print(bots[cur_symbol].get_name() + ' has put a ' + self.get_symbol(sym) + \
                          ' on ' + str(move.posx) +  ' <> ' + str(move.posy))
                new_state.is_valid(move, sym)

            except Exception as e:
                print(e)
                traceback.print_exc()
                return dict[symbols[(cur_symbol + 1) % 2]]

            cur_symbol = (cur_symbol + 1) % 2

            if verbose:
                new_state.print_board()
                if delay > 0:
                    import time
                    time.sleep(delay)


        winner = new_state.winner()
        if winner == 0 or winner == None:
            return None
        return dict[winner]



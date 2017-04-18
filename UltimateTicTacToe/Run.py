from State import State
from Engine import GameEngine
from RandomBot import RandomBot
from AlphaBetaBot import AlphaBetaBot

if __name__ == '__main__':
        r1 = RandomBot('Randomus')
        r2 = AlphaBetaBot('Alpha10')
        ge = GameEngine(r1, r2)
        n_games = 30

        ''' play only one game '''
        ''' result is the instance of the winning bot or None if it's a draw '''
        # result = ge.play(True, 0.0)
        # if result == None:
        #     print('It\'s a draw')
        # else:
        #     print('The winner is ' + result.get_name())


        ''' play n games '''
        victR1, victR2, draws = ge.play_n_games(n_games)

        print('Total number of games: ' + str(n_games))
        print(r1.get_name() + ' has won ' + str(victR1) + ' games.')
        print(r2.get_name() + ' has won ' + str(victR2) + ' games.')
        print('There were ' + str(draws) + ' draws.')
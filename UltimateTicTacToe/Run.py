from State import State
from Engine import GameEngine
from RandomBot import RandomBot

if __name__ == '__main__':
        r1 = RandomBot('Randomus')
        r2 = RandomBot('Pelangatotal')
        ge = GameEngine(r1, r2)
        n_games = 100

        # play only one game
        # result = ge.play(False, 0.1)
        # result is the instance of the winning bot or None if it's a draw

        victR1, victR2, draws = ge.play_n_games(n_games)

        print('Total number of games: ' + str(n_games))
        print(r1.get_name() + ' has won ' + str(victR1) + ' games.')
        print(r2.get_name() + ' has won ' + str(victR2) + ' games.')
        print('There were ' + str(draws) + ' draws.')
import abalone_base as ab
import abalone_model as abmod
import abalone_managers as abman
import random

#singleton Game, contains the Board, the Score and player
class Game:
    class __Game:
        def __init__(self, player_color):
            self.player_color = player_color
            self.score = abmod.Score()
            self.board = abmod.Board()
            self.board.init_pieces(self.player_color, "CLASSIC")
            self.move_manager = abman.MoveManager()
        @property
        def player_color(self):
            return self.__player_color
        @player_color.setter
        def player_color(self, player_color):
            if isinstance(player_color, ab.Color):
                self.__player_color = player_color
            else:
                self.__player_color = ab.Color.BLACK

        def __str__(self):
            return repr(self) + self.player_color
    _instance = None
    def __init__(self, player_color):
        if not Game._instance:
            Game._instance = Game.__Game(player_color)
        else:
            Game._instance.player_color = player_color
    def __str__(self):
        return str(self.__instance)
    @property
    def player_color(self):
        return self._instance.player_color

    @property
    def score(self):
        return self._instance.score

    @property
    def board(self):
        return self._instance.board

    def do_move(self, move):
        self._instance.move_manager.do_move(move)

    #function: get_moves, returns list of possible moves
    def get_moves(self, color):
        return self._instance.move_manager.get_moves(color)

#------------------------------------------------------------------------------

def main():
    game = Game(ab.Color.BLACK)
    # for _ in range(500):
    #     for color in ab.Color.__members__.values():
    #         moves = game.get_moves(color)
    #         move = random.choice(moves)
    #         game.do_move(move)
    #         print(game.board)
    #         print(move)
    #         print(game.score)

    moves = game.get_moves(ab.Color.BLACK)
    print("number of possible moves: {}".format(len(moves)))

    print(game.board)
    print("------------")
    move = ab.Move(ab.Position(1, 5), ab.Position(3, 5), ab.Direction.RIGHT_DOWN)
    game.do_move(move)

    print(game.board)
    print("------------")
    move = ab.Move(ab.Position(8, 5), ab.Position(7, 5), ab.Direction.RIGHT_UP)
    game.do_move(move)

    print(game.board)
    print("------------")
    move = ab.Move(ab.Position(2, 5), ab.Position(4, 5), ab.Direction.RIGHT_DOWN)
    game.do_move(move)

    print(game.board)
    print("------------")
    move = ab.Move(ab.Position(3, 5), ab.Position(5, 5), ab.Direction.RIGHT_DOWN)
    game.do_move(move)

    print(game.board)
    print("------------")
    move = ab.Move(ab.Position(4, 5), ab.Position(6, 5), ab.Direction.RIGHT_DOWN)
    game.do_move(move)

    print(game.board)
    print(move)
    print(game.score)
    print("------------")

    move = ab.Move(ab.Position(5, 5), ab.Position(7, 5), ab.Direction.RIGHT_DOWN)
    game.do_move(move)
    print(game.board)
    print(move)
    print(game.score)
    print("------------")

    print(abman.MoveParser().parse_from_move_string("d5,c5"))

    move = ab.Move(ab.Position(6, 5), ab.Position(8, 5), ab.Direction.RIGHT_DOWN)

    print(abman.MoveParser().parse_to_move_string(move))

    game.do_move(move)
    print(game.board)
    print(move)



    print(game.score)
    print("------------")

    moves = game.get_moves(ab.Color.WHITE)
    [print(move) for move in moves]
    print("number of possible moves: {}".format(len(moves)))

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

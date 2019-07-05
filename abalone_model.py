import abalone_base as ab
import abalone_starting_positions as absp

#singleton Score, contains game score
class Score:
    class __Score:
        def __init__(self):
            self.score_black = 0
            self.score_white = 0
    _instance = None
    def __init__(self):
        if not Score._instance:
            Score._instance = Score.__Score()

    def get_score(self, color):
        if color is ab.Color.BLACK:
            return self._instance.score_black
        if color is ab.Color.WHITE:
            return self._instance.score_white

    def increment_score(self, color):
        if not self.game_over:
            if color is ab.Color.BLACK:
                self._instance.score_black += 1
            if color is ab.Color.WHITE:
                self._instance.score_white += 1

    @property
    def game_over(self):
        if self.get_score(ab.Color.BLACK) == 6 or self.get_score(ab.Color.WHITE) == 6:
            return True
        return False

    def __str__(self):
        return 'BLACK: {} - WHITE: {}'.format(str(self.get_score(ab.Color.BLACK)), str(self.get_score(ab.Color.WHITE)))

#singleton Board, contains Fields, function: get_field(position), fields iterator
class Board:
    class __Board:
        def __init__(self, outer_self):
            self.rotate_board = False #something that belongs to the View class(es) but for now is placed here
            self.init_board(outer_self)

        def init_board(self, outer_self):
            self.fields = {}

            for x in range(Board._SIZE):
                for y in range(Board._SIZE):
                    position = ab.Position(x, y)
                    if(x == 0 or x == 10 or y == 0 or y == 10 or x + y <= 5 or x + y >= 15):
                        type_ = ab.FieldType.GUTTER
                    else:
                        type_ = ab.FieldType.BOARD
                    field = ab.Field(outer_self, type_, position)   #pass Board-instance: outer_self to each Field-object
                    self.fields[position] = field

        def init_pieces(self, player_color, board_style):
            self.player_pieces = []
            self.opponent_pieces = []

            player_positions = absp.CLASSIC_PLAYER
            for piece_position in player_positions:
                field = self.fields[piece_position]
                piece = ab.Piece(player_color, field)
                field.piece = piece
                self.player_pieces.append(piece)

            opponent_color = ab.Color.BLACK
            if player_color == ab.Color.BLACK:
                opponent_color = ab.Color.WHITE

            opponent_positions = absp.CLASSIC_OPPONENT
            for piece_position in opponent_positions:
                field = self.fields[piece_position]
                piece = ab.Piece(opponent_color, field)
                field.piece = piece
                self.opponent_pieces.append(piece)

    _instance = None
    _SIZE = 11
    def __init__(self):
        if not Board._instance:
            Board._instance = Board.__Board(self) #pass Board-instance: self to inner class __Board

    def __str__(self):
        return str(self._instance)

    def init_pieces(self, player_color, board_style):
        self._instance.init_pieces(player_color, board_style)

    def field_adjacent_to(self, field, direction):
        position = self.position_adjacent_to(field.position, direction)
        return self.field(position)

    @staticmethod
    def position_adjacent_to(position, direction):
        if not isinstance(direction, ab.Direction):
            return (-1,-1)
        if direction is ab.Direction.LEFT:
            return position + ab.DIRECTION_VECTORS[ab.Direction.LEFT]
        if direction is ab.Direction.LEFT_DOWN:
            return position + ab.DIRECTION_VECTORS[ab.Direction.LEFT_DOWN]
        if direction is ab.Direction.LEFT_UP:
            return position + ab.DIRECTION_VECTORS[ab.Direction.LEFT_UP]
        if direction is ab.Direction.RIGHT:
            return position + ab.DIRECTION_VECTORS[ab.Direction.RIGHT]
        if direction is ab.Direction.RIGHT_DOWN:
            return position + ab.DIRECTION_VECTORS[ab.Direction.RIGHT_DOWN]
        if direction is ab.Direction.RIGHT_UP:
            return position + ab.DIRECTION_VECTORS[ab.Direction.RIGHT_UP]

    @staticmethod
    def direction(tail_position, head_position):
        if not isinstance(tail_position, ab.Position) or not isinstance(head_position, ab.Position):
            return None
        if tail_position + ab.DIRECTION_VECTORS[ab.Direction.LEFT] == head_position:
            return ab.Direction.LEFT
        if tail_position + ab.DIRECTION_VECTORS[ab.Direction.LEFT_DOWN] == head_position:
            return ab.Direction.LEFT_DOWN
        if tail_position + ab.DIRECTION_VECTORS[ab.Direction.LEFT_UP] == head_position:
            return ab.Direction.LEFT_UP
        if tail_position + ab.DIRECTION_VECTORS[ab.Direction.RIGHT] == head_position:
            return ab.Direction.RIGHT
        if tail_position + ab.DIRECTION_VECTORS[ab.Direction.RIGHT_DOWN] == head_position:
            return ab.Direction.RIGHT_DOWN
        if tail_position + ab.DIRECTION_VECTORS[ab.Direction.RIGHT_UP] == head_position:
            return ab.Direction.RIGHT_UP
        return None

    @staticmethod
    def opposite_direction(direction):
        for opposite_direction, opposite_direction_vector in ab.DIRECTION_VECTORS.items():
            direction_vector = Board().position_adjacent_to(ab.Position(0,0), direction)
            if direction_vector + opposite_direction_vector == ab.Position(0,0):
                return opposite_direction

    def field(self, position):
        try:
            field = self._instance.fields[position]
        except KeyError as e:
            #print('I got a KeyError - reason {}'.format(str(e)))
            field = None
        except:
            print('I got another exception, but I should re-raise')
            raise
        return field

    def __str__(self):                      #something that belongs to the View class(es) but for now is placed here
        def get_field_string(x, y):
            field = self.field((x,y))
            if field.type_ == ab.FieldType.GUTTER:
                return 'x  '
            elif field.type_ == ab.FieldType.BOARD and not field.piece:
                return '.  '
            elif field.piece:
                if field.piece.color == ab.Color.BLACK:
                    return '@  '
                elif field.piece.color == ab.Color.WHITE:
                    return 'O  '

        s = ''
        if self.rotate_board:
            for x in range(10,-1,-1):
                for y in range(10, -1, -1):
                    s += get_field_string(x,y)
                s += '\n'
        else:
            for x in range(11):
                for y in range(11):
                    s += get_field_string(x,y)
                s += '\n'
        return(s)

    @property
    def rotate_board(self):                 #something that belongs to the View class(es) but for now is placed here
        return self._instance.rotate_board
    @rotate_board.setter
    def rotate_board(self, rotate_board):   #something that belongs to the View class(es) but for now is placed here
        self._instance.rotate_board = rotate_board

    def __iter__(self):
        return iter(self._instance.fields.values())

    def pieces(self, color):
        for field in self:
            if field.piece and field.piece.color == color:
                yield field.piece

    def clear_marked_pieces(self):
        for color in ab.Color.__members__.values():
            for piece in self.pieces(color):
                piece.marked = False

    def clear_gutter(self):
        for field in self:
            if not field.is_empty and field.type_ == ab.FieldType.GUTTER:
                Score().increment_score(field.piece.color)
                field.piece = None

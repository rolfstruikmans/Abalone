from enum import Enum, auto

class Combo(Enum):
    SINGLE = auto()
    DUO = auto()
    TRIPLE = auto()

class Color(Enum):
    BLACK = auto()
    WHITE = auto()

class FieldType(Enum):
    GUTTER = auto()
    BOARD = auto()

class Direction(Enum):
    LEFT_DOWN = auto()
    LEFT = auto()
    LEFT_UP = auto()
    RIGHT_UP = auto()
    RIGHT = auto()
    RIGHT_DOWN = auto()

class Position(tuple):
    def __new__(cls, x, y):
        return tuple.__new__(Position, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __add__(self, value):
        return Position(self.x + value.x, self.y + value.y)

DIRECTION_VECTORS = {Direction.LEFT: Position(0,-1), Direction.LEFT_DOWN:Position(1,-1), Direction.LEFT_UP:Position(-1,0), Direction.RIGHT:Position(0,1), Direction.RIGHT_DOWN:Position(1,0), Direction.RIGHT_UP:Position(-1,1)}

#class Field, contains position, type: {GUTTER, BOARD}, piece
class Field:
    def __init__(self, board, type_, position, piece = None):
        self._board = board
        self._type_ = type_
        self._position = position
        self._piece = piece

    @property
    def type_(self):
        return self._type_
    @type_.setter
    def type(self, type_):
        if isinstance(type_, FieldType):
            self._type_ = type_
        else:
            self._type_ = FieldType.GUTTER
    @property
    def position(self):
        return self._position
    @property
    def piece(self):
        return self._piece
    @piece.setter
    def piece(self, piece):
        self._piece = piece
        if self._piece:
            self._piece.field = self

    def adjacent_field(self, direction):
        return self._board.field_adjacent_to(self, direction)

    def __eq__(self, field):
        return field and (self.position == field.position)

    @property
    def is_empty(self):
        return not self.piece

#class: piece, containing color, marked
class Piece:
    def __init__(self, color, field):
        self.marked = False
        self._color = color
        self.field = field

    @property
    def color(self):
        return self._color

#class: Move, contains everything that defines a move
class Move(tuple):
    def __new__(cls, tail_position, head_position, direction):
        if  not isinstance(tail_position, Position) or not isinstance(head_position, Position) or not isinstance(direction, Direction):
            return tuple.__new__(Move, (Position(-1,-1), Position(-1,-1), Direction.NONE))
        return tuple.__new__(Move, (tail_position, head_position, direction))

    @property
    def tail_position(self):
        return self[0]

    @property
    def head_position(self):
        return self[1]

    @property
    def direction(self):
        return self[2]

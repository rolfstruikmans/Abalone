import abalone_base as ab
import abalone_model as abmod

class MoveParser:   #parses move-strings to Move-objects and visa versa
    class __MoveParser:
        def __init__(self):
            self.board = abmod.Board()
    _instance = None
    _ROWS = '_ihgfedcba_'

    def __init__(self):
        if not MoveParser._instance:
            MoveParser._instance = MoveParser.__MoveParser()

    @property
    def board(self):
        return self._instance.board

    #a1-b2,a2 or a1,a2
    def parse_from_move_string(self, move_string):
        tail_position = ab.Position(MoveParser._ROWS.index(move_string[0]),int(move_string[1]))
        if move_string[2] == '-':
            head_position = ab.Position(MoveParser._ROWS.index(move_string[3]),int(move_string[4]))
            desitination_position = ab.Position(MoveParser._ROWS.index(move_string[6]),int(move_string[7]))
            move_direction = self.board.direction(tail_position, head_position)
            return ab.Move(tail_position, head_position, move_direction)
        elif move_string[2] == ',':
            desitination_position = ab.Position(MoveParser._ROWS.index(move_string[3]),int(move_string[4]))
            move_direction = self.board.direction(tail_position, desitination_position)
            field = self.board.field(tail_position)
            if field and not field.is_empty:
                color = field.piece.color
                while field and not field.is_empty and field.piece.color == color:
                    previous_field = field
                    field = field.adjacent_field(move_direction)
                return ab.Move(tail_position, previous_field.position, move_direction)
        return None

    def parse_to_move_string(self, move):
        source = MoveParser._ROWS[move.tail_position.x] + str(move.tail_position.y)
        if (move.tail_position != move.head_position) and not MoveManager().is_inline_move(move):
            source += '-' + ROWS[move.head_position.x] + str(move.head_position.y)
        desitination_position = move.tail_position + ab.DIRECTION_VECTORS[move.direction]
        dest = MoveParser._ROWS[desitination_position.x] + str(desitination_position.y)
        move_string = source + ',' + dest
        return move_string





class MoveManager:
    class __MoveManager:
        def __init__(self):
            self.board = abmod.Board()

    _instance = None

    def __init__(self):
        if not MoveManager._instance:
            MoveManager._instance = MoveManager.__MoveManager()

    @property
    def board(self):
        return self._instance.board

    def _get_combo_direction(self, tail_field, head_field): #combo_direction is in the direction from tail_field to head_field
        if not isinstance(tail_field, ab.Field) or not isinstance(head_field, ab.Field):
            return None  #check whether parameters are Field-objects
        if tail_field == head_field:
            return None
        direction = self.board.direction(tail_field.position, head_field.position)  #get direction of adjacent field positions
        if direction:   #tail_field and head_field are adjacent
            return direction
        for direction in ab.Direction.__members__.values():   #tail_field and head_field should be two steps apart
            if head_field == tail_field.adjacent_field(direction).adjacent_field(direction): #get field two steps from tail_field in direction: "dir" (this only works for tail_fields being BOARD-fields, not GUTTER-fields)
                return direction
        return None

    def _get_combo(self, tail_field, head_field):   #returns SINGLE in case of a single field, DUO in case of two adjacent fields and TRIPLE in case of three aligned adjacent fields, None otherwise
        if not isinstance(tail_field, ab.Field) or not isinstance(head_field, ab.Field):
            return None  #check whether parameters are Field-objects
        if tail_field == head_field:
            return ab.Combo.SINGLE
        direction = self._get_combo_direction(tail_field, head_field)
        if direction:
            if tail_field.adjacent_field(direction) == head_field:
                return ab.Combo.DUO
            return ab.Combo.TRIPLE
        return None

    def _is_valid_combo(self, tail_field, head_field):
        if not isinstance(tail_field, ab.Field) or not isinstance(head_field, ab.Field):
            return False  #check whether parameters are Field-objects
        if tail_field.is_empty or head_field.is_empty:
            return False    #check whether both positions contain a piece
        combo = self._get_combo(tail_field, head_field)
        if combo == ab.Combo.SINGLE:
            return True #since tail_field contains a piece
        if combo == ab.Combo.DUO:
            return tail_field.piece.color == head_field.piece.color
        if combo == ab.Combo.TRIPLE:
            combo_direction = self._get_combo_direction(tail_field, head_field)   #get alignment direction
            middle_field = tail_field.adjacent_field(combo_direction) #since combo is TRIPLE this middle_field and direction is garanteed to exist
            if not middle_field.is_empty:
                return tail_field.piece.color == middle_field.piece.color == head_field.piece.color
        return False

    def is_valid(self, move): #returns True if move is a valid move, False otherwise
        def is_valid_inline_move():
            if combo == ab.Combo.DUO:
                return is_empty_board_field(field_a) or is_opponent_and_empty_field(field_a, field_b)
            if combo == ab.Combo.TRIPLE:
                return is_empty_board_field(field_a) or is_opponent_and_empty_field(field_a, field_b) or is_two_opponents_and_empty_field(field_a, field_b, field_c)

        def is_valid_sideways_move():
            if combo == ab.Combo.DUO:
                return is_empty_board_field(field_a) and is_empty_board_field(field_b)
            if combo == ab.Combo.TRIPLE:
                return is_empty_board_field(field_a) and is_empty_board_field(field_b) and is_empty_board_field(field_c)

        def is_empty_board_field(field):
            if not field:
                return False
            return field.is_empty and field.type_ == ab.FieldType.BOARD

        def is_opponent_and_empty_field(field_a, field_b):
            if not field_a or not field_b:
                return False
            return not field_a.is_empty and field_a.piece.color != color and field_b.is_empty

        def is_two_opponents_and_empty_field(field_a, field_b, field_c):
            if not field_a or not field_b or not field_c:
                return False
            return not field_a.is_empty and field_a.piece.color != color and not field_b.is_empty and field_b.piece.color != color and field_c.is_empty

        tail_field = self.board.field(move.tail_position)
        head_field = self.board.field(move.head_position)

        if not tail_field or not head_field or not move.direction:
            return False  #check whether both positions are field positions and move.direction is given
        if not self._is_valid_combo(tail_field, head_field):
            return False
        #we have a valid combo
        combo = self._get_combo(tail_field, head_field)

        if combo == ab.Combo.SINGLE:
            desitination_field = tail_field.adjacent_field(move.direction)
            return desitination_field.type_ == ab.FieldType.BOARD and desitination_field.is_empty

        color = tail_field.piece.color  #this is the color of all pieces in the combo
        combo_direction = self._get_combo_direction(tail_field, head_field)

        inline = self.is_inline_move(move) #inline or sideways movement
        if combo_direction == self.board.opposite_direction(move.direction):    #inline movement in opposite direction (tail_position and head_position are switched and thus incorrect)
            return False

        #set fields involved in movement
        field_a = None
        field_b = None
        field_c = None

        if combo == ab.Combo.DUO:
            if inline:
                field_a = head_field.adjacent_field(move.direction)
                if field_a:
                    field_b = field_a.adjacent_field(move.direction)
            else:   #sideways movement
                field_a = tail_field.adjacent_field(move.direction)
                field_b = head_field.adjacent_field(move.direction)

        if combo == ab.Combo.TRIPLE:
            if inline:
                field_a = head_field.adjacent_field(move.direction)
                if field_a:
                    field_b = field_a.adjacent_field(move.direction)
                    if field_b:
                        field_c = field_b.adjacent_field(move.direction)
            else:   #sideways movement
                field_a = tail_field.adjacent_field(move.direction)
                middle_field = tail_field.adjacent_field(combo_direction)    #since combo is TRIPLE, this middle_field is garanteed to exist
                field_b = middle_field.adjacent_field(move.direction)
                field_c = head_field.adjacent_field(move.direction)

        if inline:
            return is_valid_inline_move()
        else:
            return is_valid_sideways_move()

    def do_move(self, move):
        if not self.is_valid(move):
            print("invalid move")
            return

        tail_field = self.board.field(move.tail_position)
        head_field = self.board.field(move.head_position)

        combo_direction = self._get_combo_direction(tail_field, head_field)
        inline = self.is_inline_move(move)

        if inline:
            self._do_inline_move(tail_field, head_field, move.direction)
        else:
            self._do_sideways_move(tail_field, head_field, move.direction, combo_direction)

        self.board.clear_gutter()

    def _do_inline_move(self, tail_field, head_field, move_direction):
        empty_field = head_field
        while not empty_field.is_empty:
            empty_field = empty_field.adjacent_field(move_direction)
        opposite_move_direction = self.board.opposite_direction(move_direction)
        source_field = empty_field.adjacent_field(opposite_move_direction)
        while empty_field is not tail_field:
            empty_field.piece = source_field.piece
            source_field.piece = None
            empty_field = source_field
            source_field = empty_field.adjacent_field(opposite_move_direction)

    def _do_sideways_move(self, tail_field, head_field, move_direction, combo_direction):
        source_field = tail_field
        desitination_field = source_field.adjacent_field(move_direction)
        desitination_field.piece = source_field.piece
        source_field.piece = None
        while source_field != head_field:
            source_field = source_field.adjacent_field(combo_direction)
            desitination_field = source_field.adjacent_field(move_direction)
            desitination_field.piece = source_field.piece
            source_field.piece = None

    def get_moves(self, color):
        moves = []

        #get moves of all single pieces
        for piece in self.board.pieces(color) :
            for direction in ab.Direction.__members__.values():
                move = ab.Move(piece.field.position, piece.field.position, direction)
                if self.is_valid(move):
                    moves.append(move)

        #get moves of all duos
        for piece in self.board.pieces(color) :
            for direction in ab.Direction.__members__.values():
                field = piece.field.adjacent_field(direction)
                if field and not field.is_empty and field.piece.color == piece.color:
                    for move_direction in ab.Direction.__members__.values():
                        move = ab.Move(piece.field.position, field.position, move_direction)
                        if self.is_valid(move):
                            moves.append(move)

        #get moves of all triples
        for piece in self.board.pieces(color) :
            for direction in ab.Direction.__members__.values():
                middle_field = piece.field.adjacent_field(direction)
                if middle_field:
                    field = middle_field.adjacent_field(direction)
                    if field and not middle_field.is_empty and middle_field.piece.color == piece.color and not field.is_empty and field.piece.color == piece.color:
                        for move_direction in ab.Direction.__members__.values():
                            move = ab.Move(piece.field.position, field.position, move_direction)
                            if self.is_valid(move):
                                moves.append(move)

        self._remove_duplicates(moves)
        return moves

    def _remove_duplicates(self, moves):    #this works because there is at most one duplicate for a move!!!
        for move in moves:
            if move.tail_position != move.head_position:
                duplicate_move = ab.Move(move.head_position, move.tail_position, move.direction)  #a duplicate move is a move in the same direction but with head- and tail-positions swapped
                try:
                    moves.remove(duplicate_move)
                except ValueError:
                    pass

    def is_inline_move(self, move):
        tail_field = self.board.field(move.tail_position)
        head_field = self.board.field(move.head_position)
        combo_direction = self._get_combo_direction(tail_field, head_field)
        return combo_direction == move.direction

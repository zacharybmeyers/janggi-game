import random
import logging

from janggi.board import Board
from janggi.utils import algebraic_to_numeric, numeric_to_algebraic


class Game:
    """Represents a game of Janggi"""
    def __init__(self):
        """
        Initializes private data members for:
            game state, current turn
        Sets up the positions for every Piece.
        """
        self._game_state = "UNFINISHED"
        self._turn = "b"        # blue starts the game
        self._board = Board()

    # ATTRIBUTE GETTERS & SETTERS

    def get_game_state(self):
        """getter for game state"""
        return self._game_state

    def set_game_state(self, game_state):
        """setter for game state, where game_state is a string"""
        self._game_state = game_state

    def get_turn(self):
        """getter for turn"""
        return self._turn

    def get_turn_long(self):
        return { 'b': 'blue', 'r': 'red' }[self._turn]

    def set_turn(self, color):
        """setter for turn"""
        self._turn = color

    def update_turn(self):
        """helper function updates the turn from 'r' to 'b' and vice versa"""
        if self.get_turn() == "b":
            self.set_turn("r")
        elif self.get_turn() == "r":
            self.set_turn("b")

    def get_board(self):
        return self._board

    def is_in_check(self, color):
        return self._board.is_in_check(color)

    # ACTIONS

    def make_ai_move(self, level):
        assert (self.get_game_state() == "UNFINISHED")

        moves = self._board.all_player_moves(self.get_turn())
        invalid_moves = set()

        while True:
            start_num = None
            end_num = None

            # Find move that causes check
            # if level >= 20:
            #    for s,ends in moves.items():
            #        for e in ends:
            #            p = self._board.get_square_contents(e)
            #            if p is not None:
            #                pass

            # Find move with highest capture value
            if start_num is None and level >= 10:
                max_capture = 0
                for s, ends in moves.items():
                    for e in ends:
                        if (s, e) in invalid_moves:
                            continue  # skip previously tried invalid moves
                        if s == e:
                            continue  # skip pass moves
                        p = self._board.get_square_contents(numeric_to_algebraic(e))
                        if p is not None:
                            if p.get_worth() > max_capture:
                                (start_num, end_num) = (s, e)
                                max_capture = p.get_worth()
                if start_num is not None:
                    logging.debug('AI found max-capture={} with {} -> {}'.format(
                        max_capture, numeric_to_algebraic(start_num),
                        numeric_to_algebraic(end_num)))
                else:
                    logging.debug('AI failed to find max-capture')

            # Find random move
            if start_num is None:
                assert (end_num is None)
                start_num = random.choice(list(moves.keys()))
                end_num = random.choice(moves[start_num])
                logging.debug('AI trying random move {} -> {}'.format(
                    numeric_to_algebraic(start_num),
                    numeric_to_algebraic(end_num)))

            if level > 0:
                # disallow pass moves for anything other than "easy" AI
                if len(moves[start_num]) > 1:
                    while start_num == end_num:
                        end_num = random.choice(moves[start_num])
                    logging.debug('AI avoiding pass move, new move {} -> {}'.format(
                        numeric_to_algebraic(start_num),
                        numeric_to_algebraic(end_num)))

            start = numeric_to_algebraic(start_num)
            end = numeric_to_algebraic(end_num)
            if self.make_move(start, end):
                break
            else:
                invalid_moves.add((start_num, end_num))

        return (start, end)

    def make_move(self, start, end):
        """
        Checks the validity of a move, uses get_valid_moves() from the Piece class instance
        found at the start square.
            Note:       each piece has a valid pass move in its set of valid moves.
                        it is treated like any other move, but won't remove the piece.
            Invalid if: start square is empty (None), not the starting square's turn,
                        game is finished, end square is not in the valid moves of the
                        Piece instance from the start square, the hypothetical move
                        causes the general to be in (or remain in) check.
                        Return False if any of the invalid conditions are True.
            If valid:   move Piece object from start square to end square
                        (removes opposing piece or fills empty square),
                        update moved Piece object's position, clear start square
            Win check:  Look for checkmate on opposite player's General, if True
                        update game_state accordingly to reflect current player won.
            End:        update turn for next player, return True
        :param start: algebraic coordinate for the start square
        :param end: algebraic coordinate for the end square
        :return: True if valid move, False otherwise
        """
        # for debugging
        logging.debug(f"Attempting: {start} -> {end}")

        # INVALID CONDITIONS
        # get the Piece from the start square
        piece_obj = self._board.get_square_contents(start)
        if piece_obj is None:
            return False  # invalid move if there's no piece
        if self.get_turn() != piece_obj.get_color():  # invalid move if not starting square's turn
            return False
        if self.get_game_state() != "UNFINISHED":  # invalid move if game is finished
            return False
        end_tup = algebraic_to_numeric(end)
        if end_tup not in piece_obj.get_valid_moves():  # invalid if end position is not valid for this piece
            return False

        # initialize colors for the current and next player,
        # convert single letters to full words to use with is_in_check() method
        current_color = self.get_turn()
        if current_color == "b":
            current_color_for_check = "blue"
            next_color = "r"
            next_color_for_check = "red"
        else:
            current_color_for_check = "red"
            next_color = "b"
            next_color_for_check = "blue"

        # At this point, the current player's move is in their valid move set, but...
        #   If this move ends with the current player's general in check, invalid move
        if self._board.hypothetical_move(start, end) is False:
            return False

        #  If the valid move is a pass move (and it hasn't put or left the player in check),
        #  simply update turn and return True
        if start == end:
            logging.info(f'{current_color} moved: pass')
            self.update_turn()
            return True

        # otherwise, VALID MOVE
        start_tup = algebraic_to_numeric(start)
        start_row, start_col = start_tup
        end_row, end_col = end_tup  # unpack end square tup
        board = self._board.get_board()  # get board

        # move Piece object to new square
        # (removes opposing piece or fills empty square)
        board[end_row][end_col] = piece_obj
        piece_obj.set_position(end)  # store new position (algebraic coordinate)
        board[start_row][start_col] = None  # clear start square

        # if the next player is in check...
        # try to determine checkmate: make use of hypothetical_move() helper
        checkmate = None
        if self._board.is_in_check(next_color_for_check):
            # initialize checkmate to True
            checkmate = True
            enemy_general = self._board.get_general(next_color)
            enemy_general_pos = enemy_general.get_position()
            for move in enemy_general.get_valid_moves():
                # try a hypothetical move
                potential_move_pos = numeric_to_algebraic(move)
                if self._board.hypothetical_move(enemy_general_pos, potential_move_pos):
                    checkmate = False  # if a general can hypothetically move, not in checkmate

        if checkmate:
            if self.get_turn() == "b":
                self.set_game_state("BLUE_WON")
            elif self.get_turn() == "r":
                self.set_game_state("RED_WON")

        # update turn
        logging.info(f'{current_color} moved: {start} -> {end}')
        self.update_turn()
        return True


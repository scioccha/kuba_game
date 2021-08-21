# Author: Alexandra Sciocchetti
# Date: 5/22/2021
# Description: Contains a class named KubaGame for playing a board game called Kuba. Rules for the
# game can be found here: https://sites.google.com/site/boardandpieces/list-of-games/kuba
# Any player can start the game, and the game ends when a player wins, or the other player has no
# legal moves.

import copy
class KubaGame:
    '''represents a game call Kuba which can be played as described in the description'''
    def __init__(self, player1, player2):
        '''initializes both players, creates the board, and initializes other starting positions to None'''
        self._player1 = player1
        self._player2 = player2
        self._winner = None
        self._player_turn = None
        self._player1_captured = 0
        self._player2_captured = 0
        self._board = [["W", "W", "X", "X", "X", "B", "B"], ["W", "W", "X", "R", "X", "B", "B"],
                       ["X", "X", "R", "R", "R", "X", "X"], ["X", "R", "R", "R", "R", "R", "X"],
                       ["X", "X", "R", "R", "R", "X", "X"], ["B", "B", "X", "R", "X", "W", "W"],
                       ["B", "B", "X", "X", "X", "W", "W"]]
        self._board_2moves_prev = None
        self._board_1move_prev = None
        self._board_potential_move = None

    def get_printed_board(self):
        '''returns formatted structure of current game board, for testing purposes'''
        return ('\n'.join(['\t'.join([str(square) for square in row]) for row in self._board]))

    def get_board(self):
        '''returns board without additional formatting'''
        return self._board

    def get_board_2moves_prev(self):
        '''returns board two moves previous to current move'''
        return self._board_2moves_prev

    def get_board_1move_prev(self):
        '''returns board 1 move previous to current move'''
        return self._board_1move_prev

    def get_board_potential_move(self):
        '''returns board used to track potential moves'''
        return self._board_potential_move

    def set_board_2moves_prev(self, board):
        '''sets the game board that occurred 2 moves previously'''
        self._board_2moves_prev = board

    def set_board_1move_prev(self, board):
        '''sets the game board that occurred 1 move previously'''
        self._board_1move_prev = board

    def set_board_potential_move(self):
        '''sets the potential move game board to a deep copy of the current game board'''
        self._board_potential_move = copy.deepcopy(self.get_board())

    def get_player_color(self, player_name):
        '''returns the color being played by the player name'''
        if player_name == self._player1[0]:
            return self._player1[1]
        if player_name == self._player2[0]:
            return self._player2[1]

    def set_winner(self, player_name):
        '''sets the winner of the game'''
        self._winner = player_name

    def get_winner(self):
        '''returns the player that won the game, or None if the game is not complete'''
        return self._winner

    def get_marble(self, coords):
        '''returns the marble present at the specified coordinates or X is the space is empty'''
        row = coords[0]
        column = coords[1]
        return self._board[row][column]

    def set_captured(self, player_name):
        '''takes the player's name and adds one to that player's captured marble count'''
        if player_name == self._player1[0]:
            self._player1_captured += 1
        if player_name == self._player2[0]:
            self._player2_captured += 1

    def get_captured(self, player_name):
        '''takes the player's name and returns the number of Red marbles captured by the player'''
        if player_name == self._player1[0]:
            return self._player1_captured
        if player_name == self._player2[0]:
            return self._player2_captured

    def get_marble_count(self):
        '''returns the number of White marbles, Black marbles, and Red marbles on the board as a tuple'''
        marble_count = [0, 0, 0]
        for row in range(0, 7):
            for column in range(0, 7):
                if self.get_board()[row][column] == "W":
                    marble_count[0] += 1
                if self.get_board()[row][column] == "B":
                    marble_count[1] += 1
                if self.get_board()[row][column] == "R":
                    marble_count[2] += 1
        return (marble_count[0], marble_count[1], marble_count[2])

    def set_current_turn(self, player_name):
        '''sets the current turn'''
        self._player_turn = player_name

    def get_current_turn(self):
        '''returns the player name whose turn it currently is'''
        return self._player_turn

    def get_other_player(self, player_name):
        '''returns the name of the other player playing (not player_name)'''
        if player_name == self._player1[0]:
            return self._player2[0]
        if player_name == self._player2[0]:
            return self._player1[0]

    def direction_value(self, direction):
        '''returns directional values depending on the direction the player wishes to move'''
        if direction == "F" or direction == "L":
            return -1, -1
        if direction == "B" or direction == "R":
            return 1, 7

    def check_space(self, coords, direction):
        '''determines whether the space surrounding the selected marble allows the player to move in
        the direction specified. Returns True if a move is possible and False otherwise'''
        game_board = self.get_board()
        row = coords[0]
        column = coords[1]
        non_blanks = ["B", "W", "R"]
        dir = self.direction_value(direction)[0]
        if direction == "R" or direction == "L":
            if column - dir >= 0 and column - dir <= 6:
                if game_board[row][column - dir] in non_blanks:
                    return False
        if direction == "F" or direction == "B":
            if row - dir >= 0 and row - dir <= 6:
                if game_board[row - dir][column] in non_blanks:
                    return False
        return True

    def check_push_off_marble_color(self, player_color, coords, direction):
        '''checks whether the marble that will be pushed off the board is the same color as the
        current player. If it is the same color, returns false, otherwise returns true'''
        game_board = self.get_board()
        row = coords[0]
        column = coords[1]
        dir = self.direction_value(direction)[0]
        range_dir = self.direction_value(direction)[1]
        if direction == "F" or direction == "B":
            for i in range(row + dir, range_dir, dir):
                if game_board[i][column] == "X":
                    return True
            if game_board[range_dir - dir][column] == player_color:
                return False
        if direction == "L" or direction == "R":
            for i in range(column + dir, range_dir, dir):
                if game_board[row][i] == "X":
                    return True
            if game_board[row][range_dir - dir] == player_color:
                return False
        return True

    def check_coordinates_player_color_dir(self, player_color, coords, direction):
        '''checks whether the coordinates provided are valid, player color is valid for marble
        at given coordinates, and direction is valid'''
        game_board = self.get_board()
        row = coords[0]
        column = coords[1]
        directions = ['R', 'L', 'B', 'F']
        if row > 6 or row < 0:
            return False
        if column > 6 or column < 0:
            return False
        if game_board[row][column] != player_color:
            return False
        if direction not in directions:
            return False
        return True

    def check_player_turn(self, player_name):
        '''if player turn is None, sets player turn to the current player. Otherwise, checks to
        see if it is the current player's turn'''
        if self.get_current_turn() is None:
            self.set_current_turn(player_name)
            return True
        elif self.get_current_turn() != player_name:
            return False
        return True

    def check_for_legal_moves(self, player_name):
        '''checks to see if a player has any legal moves possible/remaining on the board,
        returns either Legal Move Possible or No Legal Moves'''
        player_color = self.get_player_color(player_name)
        player_coords = []
        possible_directions = ["F", "B", "L", "R"]
        for row in range(len(self.get_board())):
            for column in range(len(self.get_board())):
                if self.get_board()[row][column] == player_color:
                    player_coords.append((row, column))
        for item in player_coords:
            for dir in possible_directions:
                if self.check_valid_move(player_color, item, dir): #if a move is valid
                    if self.check_previous_for_win(player_name, item, dir): #if move does not undo previous move
                        return "Legal Move Possible"
        return "No Legal Moves"

    def check_previous_moves(self, player_name, coords, direction):
        '''checks to see if the current move will undo a move the opponent just made. Returns
        False if this is the case, and true otherwise'''
        game_board = self.get_board()
        self._board_2moves_prev = copy.deepcopy(self._board_1move_prev)
        self._board_1move_prev = copy.deepcopy(game_board)

        self.set_board_potential_move()
        potential_move_board = self.get_board_potential_move()

        self.move_game_piece(player_name, coords, direction, potential_move_board)
        after_potential_move = self.get_board_potential_move()
        if self.get_board_2moves_prev() is not None:
            if after_potential_move == self.get_board_2moves_prev():
                return False
        return True

    def check_previous_for_win(self, player_name, coords, direction):
        '''checks to see if a move will undo a move the opponent just made. Unlike the check_previous_moves
        function, this function is only used when checking for a win, so it does not modify the
        previous move boards'''
        board_1move_prev = self.get_board_1move_prev()
        self.set_board_potential_move()
        potential_move_board = self.get_board_potential_move()
        self.move_game_piece(player_name, coords, direction, potential_move_board)
        after_potential_move = self.get_board_potential_move()
        if board_1move_prev is not None:
            if after_potential_move == board_1move_prev:
                return False
        return True


    def check_for_a_win(self, player_name):
        '''checks if the player that just made a move has won the game. If so, sets the game winner to
        that player'''
        if self.get_captured(player_name) >= 7:
            self.set_winner(player_name)
        other_player = self.get_other_player(player_name)
        other_player_color = self.get_player_color(other_player)
        if other_player_color == "W" and self.get_marble_count()[0] == 0:
            self.set_winner(player_name)
        if other_player_color == "B" and self.get_marble_count()[1] == 0:
            self.set_winner(player_name)
        if self.check_for_legal_moves(other_player) == "No Legal Moves":
            self.set_winner(player_name)

    def check_valid_move(self, player_color, coords, direction):
        '''checks if a move is valid. Does not check whether a move undoes a previous move'''
        if self.check_coordinates_player_color_dir(player_color, coords, direction):
            if self.check_space(coords, direction):
                if self.check_push_off_marble_color(player_color, coords, direction):
                    if self.get_winner() is None:
                        return True
        return False

    def move_game_piece(self, player_name, coords, direction, board):
        '''moves a game piece at the player specified coordinates, in the player specified direction'''
        dir = self.direction_value(direction)[0]
        range_dir = self.direction_value(direction)[1]
        row = coords[0]
        column = coords[1]
        if direction == "F" or direction == "B":
            empty_coords = []
            for i in range(row + dir, range_dir, dir):
                if board[i][column] == "X":
                    empty_coords.append((i, column))
            if len(empty_coords) > 0:
                for j in range(empty_coords[0][0], row, (-1 * dir)):
                    board[j][column] = board[j - dir][column]
            if len(empty_coords) == 0:
                for j in range(range_dir - dir, row, (-1 * dir)):
                    board[j][column] = board[j - dir][column]
            board[row][column] = "X"
        if direction == "L" or direction == "R":
            empty_coords = []
            for i in range(column + dir, range_dir, dir):
                if board[row][i] == "X":
                    empty_coords.append((i, column))
            if len(empty_coords) > 0:
                for j in range(empty_coords[0][0], column, (-1 * dir)):
                    board[row][j] = board[row][j - dir]
            if len(empty_coords) == 0:
                for j in range(range_dir - dir, column, (-1 * dir)):
                    board[row][j] = board[row][j - dir]
            board[row][column] = "X"


    def make_move(self, player_name, coords, direction):
        '''verifies that a defined move is valid, it is the current players turn, and
        the move will not undo previous move. If so, makes an actual move on the game board,
        checks to see if the move pushed off any red pieces, checks for a win and sets the turn to the other
        player. Returns true unless any condition does not pass, then returns false.'''
        player_color = self.get_player_color(player_name)
        game_board = self.get_board()
        if not self.check_valid_move(player_color, coords, direction):
            return False
        if not self.check_player_turn(player_name):
            return False
        if not self.check_previous_moves(player_name, coords, direction):
            return False
        red_mable_count = self.get_marble_count()[2] #saves current red marble count
        self.move_game_piece(player_name, coords, direction, game_board) #moves the game piece
        if self.get_marble_count()[2] < red_mable_count: #checks to see if red marble count has decreased
            self.set_captured(player_name)
        self.check_for_a_win(player_name)  # check to see if player has won the game with move
        other_player = self.get_other_player(player_name)
        self.set_current_turn(other_player) #changes current turn to other player
        return True






















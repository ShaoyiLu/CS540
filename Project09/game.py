import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def check_drop_phase(self, state):
        count = 0
        for i in range(0, 5):
            for j in range(0, 5):
                if state[i][j] != " ":
                    count += 1

        return count < 8

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = self.check_drop_phase(state)

        move = []
        if not drop_phase:
            # choose a piece to move and remove it from the board
            succ_list = self.succ_move(state, self.my_piece)
            alpha = -999999
            beta = 999999
            temp_move = [(0, 0), (0, 0)]
            for suc in succ_list:
                temp_state = copy.deepcopy(state)
                temp_state[suc[0][0]][suc[0][1]] = self.my_piece
                temp_state[suc[1][0]][suc[1][1]] = ' '
                suc_value = self.min_value(temp_state, 0, alpha, beta)
                if (alpha < suc_value):
                    temp_move = suc
                    alpha = suc_value
            move = temp_move
            return move

        # select an unoccupied space randomly
        # implement a minimax algorithm to play better
        succ_list = self.succ(state)
        alpha = -999999
        beta = 999999
        next_move = [0, 0]
        for suc in succ_list:
            col = suc[1]
            row = suc[0]
            temp_state = copy.deepcopy(state)
            temp_state[row][col] = self.my_piece
            suc_value = self.min_value(temp_state, 0, alpha, beta)
            if (alpha <= suc_value):
                next_move = [row, col]
                alpha = suc_value
        move.insert(0, next_move)
        return move

    def max_value(self, state, depth, alpha, beta):
        if (self.game_value(state) != 0):
            return self.game_value(state)
        if (depth >= 1):
            return self.heuristic_game_value(state, self.my_piece)
        if (self.check_drop_phase(state)):
            succ_list = self.succ(state)
            for row, col in succ_list:
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.my_piece
                alpha = max(alpha, self.min_value(temp_state, depth + 1, alpha, beta))
        else:
            succ_list = self.succ_move(state, self.my_piece)

            for suc in succ_list:
                temp_state = copy.deepcopy(state)
                temp_state[suc[0][0]][suc[0][1]] = self.my_piece
                temp_state[suc[1][0]][suc[1][1]] = ' '
                alpha = max(alpha, self.min_value(temp_state, depth + 1, alpha, beta))

        return alpha

    def min_value(self, state, depth, alpha, beta):
        if (self.game_value(state) != 0):
            return self.game_value(state)
        if (depth >= 1):
            return self.heuristic_game_value(state, self.opp)
        if (self.check_drop_phase(state)):
            succ_list = self.succ(state)
            for row, col in succ_list:
                temp_state = copy.deepcopy(state)
                temp_state[row][col] = self.opp
                beta = min(beta, self.max_value(temp_state, depth + 1, alpha, beta))
        else:
            succ_list = self.succ_move(state, self.opp)
            for suc in succ_list:
                temp_state = copy.deepcopy(state)
                temp_state[suc[0][0]][suc[0][1]] = self.opp
                temp_state[suc[1][0]][suc[1][1]] = ' '
                beta = min(beta, self.max_value(temp_state, depth + 1, alpha, beta))
        return beta

    def succ(self, state):
        succ = []
        for row in range(5):
            for col in range(5):
                if (state[row][col] == ' '):
                    succ.append((row, col))
        random.shuffle(succ)
        return succ

    def succ_move(self, state, piece):
        move_col = [-1, 0, 1]
        move_row = [-1, 0, 1]
        succ = []
        for col in range(5):
            for row in range(5):
                if (state[row][col] == piece):
                    for m_r in move_row:
                        for m_c in move_col:
                            if (row + m_r < 5 and row + m_r >= 0 and col + m_c < 5 and col + m_c >= 0 and state[row + m_r]
                            [col + m_c] == ' '):
                                succ.append([(row + m_r, col + m_c), (row, col)])
        random.shuffle(succ)
        return succ

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for col in range(2):
            for i in range(3, 5):
                if state[i][col] != ' ' and state[i][col] == state[i - 1][col + 1] == state[i - 2][col + 2] == \
                        state[i - 3][col + 3]:
                    if state[i][col] == self.my_piece:
                        return 1
                    else:
                        return -1

        # check / diagonal wins
        for col in range(2):
            for i in range(0, 2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col + 1] == state[i + 2][col + 2] == \
                        state[i + 3][col + 3]:
                    if state[i][col] == self.my_piece:
                        return 1
                    else:
                        return -1

        # check box wins
        for col in range(0, 4):
            for i in range(0, 4):
                if state[i][col] != ' ' and state[i][col] == state[i][col + 1] == state[i + 1][col] == state[i + 1][
                    col + 1]:
                    if state[i][col] == self.my_piece:
                        return 1
                    else:
                        return -1

        return 0  # no winner yet

    def heuristic_game_value(self, state, piece):
        x = self.game_value(state)
        if (x != 0):
            return x
        max_val = -2
        min_val = 2

        for row in state:
            for col in range(2):
                temp = []
                for i in range(4):
                    temp.append(row[col + i])
                max_val = max(max_val, temp.count(self.my_piece) * 0.2)
                min_val = min(min_val, temp.count(self.opp) * 0.2 * (-1))

        for col in range(5):
            for row in range(2):
                temp = []
                for i in range(4):
                    temp.append(state[row + i][col])
                max_val = max(max_val, temp.count(self.my_piece) * 0.2)
                min_val = min(min_val, temp.count(self.opp) * (-1) * 0.2)

        for row in range(2):
            for col in range(2):
                temp = []
                for i in range(4):
                    if (row + i < 5 and col + i < 5):
                        temp.append(state[row + i][col + i])
                max_val = max(max_val, temp.count(self.my_piece) * 0.2)
                min_val = min(min_val, temp.count(self.opp) * (-1) * 0.2)

        for row in range(2):
            for col in range(3, 5):
                temp = []
                for i in range(4):
                    if (row + i < 5 and col - i >= 0):
                        temp.append(state[row + i][col - i])
                max_val = max(max_val, temp.count(self.my_piece) * 0.2)
                min_val = min(min_val, temp.count(self.opp) * (-1) * 0.2)

        for row in range(1, 4):
            for col in range(1, 4):
                temp = []
                temp.append(state[row + 1][col])
                temp.append(state[row][col + 1])
                temp.append(state[row - 1][col])
                temp.append(state[row][col - 1])
                max_val = max(max_val, temp.count(self.my_piece) * 0.2)
                min_val = min(min_val, temp.count(self.opp) * (-1) * 0.2)
        return max_val + min_val

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()

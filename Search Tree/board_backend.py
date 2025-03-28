import numpy as np

class current_board:
    def __init__(self, board = (" " * 24), white_piece = "1", black_piece = "2", total_pieces = 14):
        self.board = board
        self.white_piece = white_piece
        self.black_piece = black_piece

        self.white_pieces_on_board = 0
        self.black_pieces_on_board = 0

        self.total_pieces = total_pieces


    def display(self):
        b = self.board
        return b


    def populate_board(self):
        board_size = 24
        total_pieces = self.total_pieces
        all_points = []

        for piece in range(total_pieces):
            point_valid = False

            if (piece % 2) == 0:
                colour = self.white_piece
            else:
                colour = self.black_piece

            while point_valid == False:
                random_point = np.random.randint(0, board_size)
                if random_point not in all_points:
                    all_points.append(random_point)
                    point_valid = True
                    self.board = self.board[:random_point] + colour + self.board[random_point + 1:]

        return self.board


    def next_turn(self, colour):
        if colour == self.white_piece:
            colour = self.black_piece
        else:
            colour = self.white_piece

        return colour


    def check_row(self, point1, point2, point3):
        board = self.board

        if (board[point1] == " ") or (board[point2] == " ") or (board[point3] == " "):
            return False
        else:
            if (board[point1] == board[point2]) and (board[point1] == board[point3]):
                return True
            else:
                return False


    def board_state(self):
        board = self.board
        index = -1
        state_value = "3"

        if (self.check_row(0, 1, 2)) or (self.check_row(0, 9, 21)):
            index = 0
        elif (self.check_row(2, 14, 23)) or (self.check_row(21, 22, 23)):
            index = 23
        elif (self.check_row(1, 4, 7)) or (self.check_row(3, 4, 5)):
            index = 4
        elif (self.check_row(3, 10, 18)) or (self.check_row(9, 10, 11)):
            index = 10
        elif (self.check_row(5, 13, 20)) or (self.check_row(12, 13, 14)):
            index = 13
        elif (self.check_row(16, 19, 22)) or (self.check_row(18, 19, 20)):
            index = 19
        elif (self.check_row(6, 7, 8)) or (self.check_row(6, 11, 15)):
            index = 6
        elif (self.check_row(8, 12, 17)) or (self.check_row(15, 16, 17)):
            index = 17

        if index != -1:
            state_value = board[index]
        else:
            # No lines of 3 available
            state_value = "3"

        return state_value

    
    def all_adjacent_pieces(self):
        adj_pieces = {
            "0" : [1, 9],
            "1" : [0, 2, 4],
            "2" : [1, 14],

            "3" : [4, 10],
            "4" : [1, 3, 5, 7],
            "5" : [4, 13],

            "6" : [7, 11],
            "7" : [4, 6, 8],
            "8" : [7, 11],
            
            "9" : [0, 10, 21],
            "10" : [3, 9, 11, 18],
            "11" : [6, 10, 15],

            "12" : [8, 13, 17],
            "13" : [5, 12, 14, 20],
            "14" : [2, 13, 23],

            "15" : [11, 16],
            "16" : [15, 17, 19],
            "17" : [12, 16],

            "18" : [10, 19],
            "19" : [16, 18, 20, 22],
            "20" : [13, 19],

            "21" : [9, 22],
            "22" : [19, 21, 23],
            "23" : [14, 22],
        }

        return adj_pieces


  # def all_possible_moves(self, colour):
  #   board = self.board
  #   possible_moves = []

  #   for space in range(len(self.board)):
  #     if board[space] == " ":
  #       possible_moves.append(current_board(board[:space] + colour + board[space + 1:]))

  #   return possible_moves




if __name__ == "__main__":
    cb = current_board()
    board = cb.display()
    print(board)
    cb.populate_board()
    board = cb.display()
    print(board)

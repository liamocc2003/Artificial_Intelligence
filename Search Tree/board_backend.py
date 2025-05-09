import numpy as np

class current_board:
    def __init__(self, board = (" " * 24), white_piece = "1", black_piece = "2", total_pieces = 10):
        self.board = board
        self.white_piece = white_piece
        self.black_piece = black_piece

        self.white_pieces_on_board = self.check_num_pieces_on_board('1')
        self.black_pieces_on_board = self.check_num_pieces_on_board('2')

        self.total_pieces = total_pieces
        self.previous_rows = {}


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
                self.white_pieces_on_board += 1
            else:
                colour = self.black_piece
                self.black_pieces_on_board += 1

            while point_valid == False:
                random_point = np.random.randint(0, board_size)
                if random_point not in all_points:
                    all_points.append(random_point)
                    point_valid = True
                    self.board = self.board[:random_point] + colour + self.board[random_point + 1:]

        return self.board


    def next_turn(self, colour):
        if colour == "white":
            colour = "black"
        else:
            colour = "white"

        return colour


    def check_row(self, point1, point2, point3):
        board = self.board
        checked = None

        if (board[point1] == " ") or (board[point2] == " ") or (board[point3] == " "):
            checked = False
        else:
            if (board[point1] == board[point2]) and (board[point1] == board[point3]):
                checked = True
            else:
                checked = False
        
        return checked


    def board_state(self):
        board = self.board
        index = -1
        state_value = "3"
        all_rows = dict()


        point1 = 0
        point2 = 1
        point3 = 2
        if (self.check_row(point1, point2, point3)):
            index = 0
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 0
        point2 = 9
        point3 = 21
        if (self.check_row(point1, point2, point3)):
            index = 0
            all_rows[str(index)] = [point1, point2, point3]

        point1 = 2
        point2 = 14
        point3 = 23
        if (self.check_row(point1, point2, point3)):
            index = 23
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 21
        point2 = 22
        point3 = 23
        if (self.check_row(point1, point2, point3)):
            index = 23
            all_rows[str(index)] = [point1, point2, point3]

        point1 = 1
        point2 = 4
        point3 = 7
        if (self.check_row(point1, point2, point3)):
            index = 4
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 3
        point2 = 4
        point3 = 5
        if (self.check_row(point1, point2, point3)):
            index = 4
            all_rows[str(index)] = [point1, point2, point3]

        point1 = 3
        point2 = 10
        point3 = 18
        if (self.check_row(point1, point2, point3)):
            index = 10
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 9
        point2 = 10
        point3 = 11
        if (self.check_row(point1, point2, point3)):
            index = 10
            all_rows[str(index)] = [point1, point2, point3]

        point1 = 5
        point2 = 13
        point3 = 20
        if (self.check_row(point1, point2, point3)):
            index = 13
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 12
        point2 = 13
        point3 = 14
        if (self.check_row(point1, point2, point3)):
            index = 13
            all_rows[str(index)] = [point1, point2, point3]

        point1 = 16
        point2 = 19
        point3 = 22
        if (self.check_row(point1, point2, point3)):
            index = 19
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 18
        point2 = 19
        point3 = 20
        if (self.check_row(point1, point2, point3)):
            index = 19
            all_rows[str(index)] = [point1, point2, point3]

        point1 = 6
        point2 = 7
        point3 = 8
        if (self.check_row(point1, point2, point3)):
            index = 6
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 6
        point2 = 11
        point3 = 15
        if (self.check_row(point1, point2, point3)):
            index = 6
            all_rows[str(index)] = [point1, point2, point3]

        point1 = 8
        point2 = 12
        point3 = 17
        if (self.check_row(point1, point2, point3)):
            index = 17
            all_rows[str(index)] = [point1, point2, point3]
        point1 = 15
        point2 = 16
        point3 = 17
        if (self.check_row(point1, point2, point3)):
            index = 17
            all_rows[str(index)] = [point1, point2, point3]


        send_previous_rows = self.previous_rows
        self.previous_rows = all_rows
        current_rows = []
        if len(all_rows) > 0:
            colour_values = []
            for entry in all_rows.keys():
                colour_as_int = int(board[int(entry)])
                if colour_as_int == 1:
                    colour_values.append("white")
                else:
                    colour_values.append("black")
                current_rows.append(all_rows[entry])

            state_value = colour_values
        else:
            # No lines of 3 available
            state_value = "3"

        return state_value, send_previous_rows, all_rows

    
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
            "8" : [7, 12],
            
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
    

    def check_game_finished(self, game_finished):
        num_black_left = self.black_pieces_on_board
        num_white_left = self.white_pieces_on_board

        if (num_black_left < 3) or (num_white_left < 3):
            game_finished = True

        return game_finished
    

    def check_num_pieces_on_board(self, colour_as_int):
        board = self.board
        piece_counter = 0

        for char in board:
            if char == colour_as_int:
                piece_counter += 1

        return piece_counter


    def all_possible_moves(self, colour_as_int):
        board = self.board
        possible_moves = []
        cant_remove = []
        adj_pieces = self.all_adjacent_pieces()
        state_value, prev_lines, current_lines = self.board_state()

        if colour_as_int == 1:
            colour_to_remove_as_int = 2
        else:
            colour_to_remove_as_int = 1

        # Moving
        for space in range(len(self.board)):
            if board[space] == str(colour_as_int):

                for adj_index in adj_pieces[str(space)]:
                    if board[adj_index] == " ":
                        board_to_use = board[:space] + " " + board[space + 1:]
                        new_board = current_board(board_to_use[:adj_index] + str(colour_as_int) + board_to_use[adj_index + 1:])
                        possible_moves.append(new_board)
        
        # Removing
        if state_value != "3":
            for value in tuple(current_lines.keys()):
                if board[int(value)] == str(colour_to_remove_as_int):
                    for board_index in current_lines[value]:
                        if board_index not in tuple(prev_lines.values()):
                            cant_remove.append(board_index)

            for space in range(len(self.board)):
                if board[space] == str(colour_to_remove_as_int):
                    if space not in cant_remove:
                        new_board = current_board(board[:space] + " " + board[space + 1:])
                        possible_moves.append(new_board)

        print(possible_moves)
        
        return possible_moves


if __name__ == "__main__":
    cb = current_board()
    board = cb.display()
    print("Default:", board)

    cb.populate_board()
    board = cb.display()
    print("Populated:", board)

    print()

    print("All possible moves:")
    all_moves = cb.all_possible_moves(1)
    for move in all_moves:
        print("-", move.display())
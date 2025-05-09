from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame as pyg
import math

from board_backend import current_board
from search_tree import search_tree_node

class play_game:
    def __init__(self, width = 600, height = 600, num_pieces = 24, board_colour = (160, 90, 30), circle_radius = 25, current_board = current_board()):
        pyg.init()
        self.width = width
        self.height = height
        self.window = None
        pyg.display.set_caption("Nine Men's Morris - Search Tree Algorithm")

        self.num_pieces = num_pieces
        self.radius = circle_radius

        self.colours = dict(white = (255, 255, 255), black = (0, 0, 0), brown = board_colour, yellow = (255, 255, 0))

        self.cb = current_board
        self.cb.populate_board()
        self.game_finished = False

        self.player_colour = None
        self.comp_colour = None

        self.selected_piece = None
        self.spaces_to_move = None
        self.move_from_pos = None

    def display(self):
        cb = self.cb

        self.player_colour = input("Do you want to play as white or black (" + cb.white_piece + "/" + cb.black_piece + "): ").capitalize()
        if self.player_colour != cb.white_piece and self.player_colour != cb.black_piece:
            print("Incorrect input! Try again")
            exit()

        if self.player_colour == cb.white_piece:
            self.player_colour = "white"
            self.comp_colour = "black"
            player_turn = True
        else:
            self.player_colour = "black"
            self.comp_colour = "white"
            player_turn = False

        self.window = pyg.display.set_mode((self.width, self.height))
        self.window.fill(self.colours["brown"])

        self.draw_starting_board()
        self.draw_populated_colours()

        if player_turn:
            run_loop = True
        else:
            run_loop = False

        remove_piece = False

        while self.game_finished == False:
            # Player's turn
            while run_loop or remove_piece:
                eventList = pyg.event.get()

                for event in eventList:
                    if event.type == pyg.QUIT:
                        run_loop = False
                        self.game_finished = True
                    
                    if event.type == pyg.MOUSEBUTTONUP:
                        mouse_position = pyg.mouse.get_pos()
                        mouse_position_x = mouse_position[0]
                        mouse_position_y = mouse_position[1]

                        if (mouse_position_x > 600) or (mouse_position_x < 0) or (mouse_position_y > 600) or (mouse_position_y < 0):
                            # Ignore input
                            pass
                        else:
                            coords = self.get_all_coords()
                            coords = coords.items()

                            for coord in coords:
                                circle_x = coord[1][0]
                                circle_y = coord[1][1]

                                # Pythagorean theorom for checking if mouse click was within a circle
                                sqaured_x = (mouse_position_x - circle_x) ** 2
                                sqaured_y = (mouse_position_y - circle_y) ** 2

                                pythag_theorom = math.sqrt(sqaured_x + sqaured_y)
                                if pythag_theorom <= self.radius:
                                    # get the name of the circle that was clicked
                                    circle_clicked = coord[0]
                                    circle_name_len = len(circle_clicked)

                                    # get the circle number
                                    circle_num = circle_clicked[-1]
                                    if circle_name_len > 6:
                                        circle_num = circle_clicked[-2] + circle_num
                                    circle_num = int(circle_num)
                                    self.selected_piece = circle_num
                                    
                                    # get the circle colour of the clicked circle
                                    circle_colour = self.get_colour_from_click(mouse_position)

                                    # Remove piece
                                    if remove_piece == True:
                                        if circle_colour == self.comp_colour:
                                            num_remove_indexes = len(cannot_remove_indexes)
                                            if self.comp_colour == "white":
                                                num_color_pieces = self.cb.white_pieces_on_board
                                            else:
                                                num_color_pieces = self.cb.black_pieces_on_board

                                            if (num_remove_indexes > 0) and (num_remove_indexes * 3 != num_color_pieces):

                                                for row in cannot_remove_indexes:
                                                    if self.selected_piece not in row:
                                                        self.remove_piece(self.selected_piece)
                                                        remove_piece = False
                                                        run_loop = False
                                            else:
                                                self.remove_piece(self.selected_piece)
                                                remove_piece = False
                                                run_loop = False

                                        else:
                                            break
                                    else:
                                        # if circle colour is the same as player colour, highlight available spaces around it
                                        if self.player_colour == circle_colour:
                                            self.spaces_to_move = self.highlight_spaces(circle_num)
                                            self.move_from_pos = self.selected_piece
                                        
                                        # move piece
                                        if circle_colour == "brown":
                                            self.move_piece(self.player_colour)
                                            can_remove, cannot_remove_indexes = self.check_row(self.player_colour)
                                            if can_remove:
                                                remove_piece = True
                                                break
                                            else:
                                                run_loop = False
                pyg.display.update()

            # Check if player won
            self.game_finished = self.cb.check_game_finished(self.game_finished)
            if self.game_finished == True:
                win_colour = self.player_colour

            # Comp's turn
            if self.game_finished == False:
                search_tree = search_tree_node(self.cb, self.comp_colour)
                print(search_tree.children)
                search_tree.min_max_value()
                print(search_tree.children)
                self.cb = search_tree.children[-1].current_board
                self.draw_populated_colours()
                run_loop = True

                # Check if comp won
                self.game_finished = self.cb.check_game_finished(self.game_finished)
                if self.game_finished == True:
                    win_colour = self.comp_colour

                
        pyg.quit()

        if win_colour == self.player_colour:
            print("Player has won.")
        else:
            print("Comp has won")


    def get_all_coords(self):
        ## Divide Board
        # Divide width of board into 7 pieces
        size_of_x_gap = self.width / 7
        space_between_x = size_of_x_gap / 2
        all_x_spaces = []
        for space in range(1, 8):
            all_x_spaces.append(int((size_of_x_gap * space) - space_between_x))

        # Divide height of board into 7 pieces
        size_of_y_gap = self.height / 7
        space_between_y = size_of_y_gap / 2
        all_y_spaces = []
        for space in range (1, 8):
            all_y_spaces.append(int((size_of_y_gap * space) - space_between_y))

        ## Place all coords in dictionary
        coord_dict = {
            "coord0" : [all_x_spaces[0], all_y_spaces[0]],
            "coord1" : [all_x_spaces[3], all_y_spaces[0]],
            "coord2" : [all_x_spaces[6], all_y_spaces[0]],

            "coord3" : [all_x_spaces[1], all_y_spaces[1]],
            "coord4" : [all_x_spaces[3], all_y_spaces[1]],
            "coord5" : [all_x_spaces[5], all_y_spaces[1]],

            "coord6" : [all_x_spaces[2], all_y_spaces[2]],
            "coord7" : [all_x_spaces[3], all_y_spaces[2]],
            "coord8" : [all_x_spaces[4], all_y_spaces[2]],

            "coord9" : [all_x_spaces[0], all_y_spaces[3]],
            "coord10" : [all_x_spaces[1], all_y_spaces[3]],
            "coord11" : [all_x_spaces[2], all_y_spaces[3]],

            "coord12" : [all_x_spaces[4], all_y_spaces[3]],
            "coord13" : [all_x_spaces[5], all_y_spaces[3]],
            "coord14" : [all_x_spaces[6], all_y_spaces[3]],

            "coord15" : [all_x_spaces[2], all_y_spaces[4]],
            "coord16" : [all_x_spaces[3], all_y_spaces[4]],
            "coord17" : [all_x_spaces[4], all_y_spaces[4]],

            "coord18" : [all_x_spaces[1], all_y_spaces[5]],
            "coord19" : [all_x_spaces[3], all_y_spaces[5]],
            "coord20" : [all_x_spaces[5], all_y_spaces[5]],

            "coord21" : [all_x_spaces[0], all_y_spaces[6]],
            "coord22" : [all_x_spaces[3], all_y_spaces[6]],
            "coord23" : [all_x_spaces[6], all_y_spaces[6]]
        }

        return coord_dict
  
    def draw_starting_board(self):
        coords = self.get_all_coords()

        ### Draw lines
            ## Outer lines
                # Outer top line
        pyg.draw.line(self.window, self.colours["black"], coords["coord0"], coords["coord2"], 3)
                # Outer side lines
        pyg.draw.line(self.window, self.colours["black"], coords["coord0"], coords["coord21"], 3)
        pyg.draw.line(self.window, self.colours["black"], coords["coord2"], coords["coord23"], 3)
                # Outer bottom line
        pyg.draw.line(self.window, self.colours["black"], coords["coord21"], coords["coord23"], 3)

            ## Between lines
                # Between top line
        pyg.draw.line(self.window, self.colours["black"], coords["coord3"], coords["coord5"], 3)
                # Between side lines
        pyg.draw.line(self.window, self.colours["black"], coords["coord3"], coords["coord18"], 3)
        pyg.draw.line(self.window, self.colours["black"], coords["coord5"], coords["coord20"], 3)
                # Between bottom line
        pyg.draw.line(self.window, self.colours["black"], coords["coord18"], coords["coord20"], 3)

            ## Inner lines
                # Inner top line
        pyg.draw.line(self.window, self.colours["black"], coords["coord6"], coords["coord8"], 3)
                # Inner side lines
        pyg.draw.line(self.window, self.colours["black"], coords["coord6"], coords["coord15"], 3)
        pyg.draw.line(self.window, self.colours["black"], coords["coord8"], coords["coord17"], 3)
                # Inner bottom line
        pyg.draw.line(self.window, self.colours["black"], coords["coord15"], coords["coord17"], 3)

            ## Inner to Outer lines
                # Top
        pyg.draw.line(self.window, self.colours["black"], coords["coord1"], coords["coord7"], 3)
                # Left
        pyg.draw.line(self.window, self.colours["black"], coords["coord9"], coords["coord11"], 3)
                # Right
        pyg.draw.line(self.window, self.colours["black"], coords["coord12"], coords["coord14"], 3)
                # Bottom
        pyg.draw.line(self.window, self.colours["black"], coords["coord16"], coords["coord22"], 3)


        ### Generate all circles for pieces
        for piece in range(self.num_pieces):
            pyg.draw.circle(self.window, self.colours["brown"], coords["coord" + str(piece)], self.radius, 0)
            pyg.draw.circle(self.window, self.colours["black"], coords["coord" + str(piece)], self.radius, 3)
    

    def draw_populated_colours(self):
        board = self.cb.display()

        for index in range(len(board)):
            # White
            if board[index] == "1":
                self.change_colour(index, "white")

            # Black
            elif board[index] == "2":
                self.change_colour(index, "black")

            else:
                self.change_colour(index, "brown")

    
    def get_colour_from_click(self, mouse_position):
        colour_from_click = []
        colour = tuple(self.window.get_at(mouse_position))
        for i in range(3):
            colour_from_click.append(colour[i])

        colour_clicked = tuple(colour_from_click)
        for colours in self.colours:
            if colour_clicked == self.colours[colours]:
                colour_clicked = colours
                break
        
        return colour_clicked

    
    def change_colour(self, circle_number, colour):
        coords = self.get_all_coords()

        if colour == "brown":
            pyg.draw.circle(self.window, self.colours["brown"], coords["coord" + str(circle_number)], self.radius, 0)
            pyg.draw.circle(self.window, self.colours["black"], coords["coord" + str(circle_number)], self.radius, 3)
        else:
            pyg.draw.circle(self.window, self.colours[colour], coords["coord" + str(circle_number)], self.radius, 0)


    def highlight_spaces(self, circle_number):
        all_pieces = []

        self.draw_populated_colours()
        circle_coords = self.get_all_coords()
        available_spots = self.cb.all_adjacent_pieces()

        spots_to_check = available_spots[str(circle_number)]
        for circle in spots_to_check:
            current_circle_coords = circle_coords["coord" + str(circle)]
            colour = self.get_colour_from_click(current_circle_coords)
            if colour == 'brown':
                all_pieces.append(circle)
            
        if len(all_pieces) > 0:
            for circle in all_pieces:
                pyg.draw.circle(self.window, self.colours["yellow"], circle_coords["coord" + str(circle)], self.radius, 3)
        
        return all_pieces

    
    def move_piece(self, colour):
        board = self.cb.display()

        if colour == "white":
            colour_moving = "1"
        else:
            colour_moving = "2"

        spaces_to_move = self.spaces_to_move
        if spaces_to_move != None:
            move_to_pos = self.selected_piece
            move_from_pos = self.move_from_pos

            if move_to_pos in spaces_to_move:
                board = board[:move_from_pos] + " " + board[move_from_pos + 1:]
                board = board[:move_to_pos] + colour_moving + board[move_to_pos + 1:]

                self.cb.board = board
        
        self.draw_populated_colours()

    
    def check_row(self, current_colour):
        state = self.cb.board_state()
        state_value = state[0]
        past_lines = state[1]
        current_lines = state[2]

        cannot_remove = []

        can_remove = False

        other_colour = self.cb.next_turn(current_colour)

        if other_colour in state_value:
            for colour_index in range(len(state_value)):
                if state_value[colour_index] == other_colour:
                    cannot_remove.append(tuple(current_lines.items())[colour_index][1])

        if current_colour in state[0]:
            if state[1] == None: 
                return

            past_lines_as_list = list(past_lines.values())
            current_lines_as_list = list(current_lines.values())


            # for each set in current_lines, check if that set is in past_lines
            # if in past, NO         if not in past, YES
            can_remove_inc = 0
            for line_set in current_lines_as_list:
                if line_set in past_lines_as_list:
                    can_remove_inc += 1
            
            if can_remove_inc != len(current_lines):
                can_remove = True
        
        return can_remove, cannot_remove

        

    
    def remove_piece(self, circle_num):
        self.change_colour(circle_num, "brown")
        self.cb.board = self.cb.board[:self.selected_piece] + " " + self.cb.board[self.selected_piece + 1:]
        if self.comp_colour == "white":
            self.cb.white_pieces_on_board -= 1
        else:
            self.cb.black_pieces_on_board -= 1



if __name__ == "__main__":
    game = play_game()
    game.display()
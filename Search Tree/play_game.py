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

    def display(self):
        cb = self.cb
        player_colour = input("Do you want to play as white or black (" + cb.white_piece + "/" + cb.black_piece + "): ").capitalize()
        if player_colour != cb.white_piece and player_colour != cb.black_piece:
            print("Incorrect input! Try again")
            exit()

        if player_colour == cb.white_piece:
            player_colour = "white"
            player_turn = True
        else:
            player_colour = "black"
            player_turn = False

        self.window = pyg.display.set_mode((self.width, self.height))
        self.window.fill(self.colours["brown"])

        self.draw_starting_board()
        self.draw_populated_colours()

        if player_turn:
            run_loop = True
        else:
            run_loop = False

        while run_loop:
            eventList = pyg.event.get()

            for event in eventList:
                if event.type == pyg.QUIT:
                    run_loop = False
                
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
                                circle_clicked = coord[0]
                                circle_name_len = len(circle_clicked)

                                circle_num = circle_clicked[-1]
                                if circle_name_len > 6:
                                    circle_num = circle_clicked[-2] + circle_num
                                circle_num = int(circle_num)
                                
                                circle_colour = self.get_colour_from_click(mouse_position)
                                self.highlight_spaces(player_colour, circle_num, circle_colour)
            pyg.display.update()
        pyg.quit()


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
            pyg.draw.circle(self.window, self.colours["black"], coords["coord" + str(circle_number)], self.radius, 3)
        else:
            pyg.draw.circle(self.window, self.colours[colour], coords["coord" + str(circle_number)], self.radius, 0)


    def highlight_spaces(self, player_colour, circle_number, circle_colour):
        all_pieces = []

        if player_colour == circle_colour:
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



if __name__ == "__main__":
    game = play_game()
    game.display()
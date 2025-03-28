from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame as pyg
import math

class current_board:
    def __init__(self, width = 600, height = 600, num_pieces = 24, board_colour = (160, 90, 30), circle_radius = 25):
        pyg.init()
        self.width = width
        self.height = height
        self.window = pyg.display.set_mode((self.width, self.height))
        pyg.display.set_caption("Nine Men's Morris - Search Tree Algorithm")
        self.num_pieces = num_pieces
        self.colours = dict(white = (255, 255, 255), black = (0, 0, 0), board = board_colour)
        self.radius = circle_radius

    def display(self):
        run_loop = True
        self.window.fill(self.colours["board"])

        current_board.draw_starting_board(self)

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
                        coords = current_board.get_all_coords(self)
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
                                for char in range(circle_name_len):
                                    circle_num = circle_clicked[-1]
                                    if circle_name_len > 6:
                                        circle_num = circle_clicked[-2] + circle_num
                                    
                                    circle_num = int(circle_num)
                                print(circle_num)

                                ## Get clicked colour
                                colour_from_click = []
                                colour = tuple(self.window.get_at(mouse_position))
                                for i in range(3):
                                    colour_from_click.append(colour[i])

                                colour_clicked = tuple(colour_from_click)
                                for colours in self.colours:
                                    if colour_clicked == self.colours[colours]:
                                        colour_clicked = colours
                                        break

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
        coords = current_board.get_all_coords(self)

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
            pyg.draw.circle(self.window, self.colours["board"], coords["coord" + str(piece)], self.radius, 0)
            pyg.draw.circle(self.window, self.colours["black"], coords["coord" + str(piece)], self.radius, 3)



# If colour clicked = player colour: highlight available spaces
#  --- Available spaces
#  --- Highlight by checking the colour of nearby spaces
#       If brown, highlight
#           -- To highlight: pass piece number, colour



if __name__ == "__main__":
    game = current_board()
    game.display()
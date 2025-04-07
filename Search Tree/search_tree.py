class search_tree_node:
    def __init__(self, board_instance, colour, ply = 0):
        self.children = []
        self.ply_depth = ply
        self.current_board = board_instance

        self.colour_as_int = colour
        if self.colour_as_int == 1:
            self.colour_as_str = "white"
        else:
            self.colour_as_str = "black"
        
        self.value_is_assigned = False


        # No line of 3
        state_value, prev_lines, current_lines = self.current_board.board_state()
        if state_value == "3":
            if self.ply_depth < 10:
                self.generate_children("no_line")
                
            if len(self.children) > 0:
                for child in self.children:
                    print(child.current_board.display())
            else:
                print(":(")
                # Stop ply_depth
                return

        # Line of 3 found
        else:
            #Line of 3 for colour
            if self.colour_as_str in state_value:
                print("For Colour: " + self.colour_as_str)
            # Line of 3 for other colour
            else:
                print("Other Colour: " + self.colour_as_str)
                
            self.generate_children("line")

            if ((self.ply_depth % 2) == 0):
                self.value = -1
            else:
                self.value = 1
            self.value_is_assigned = True


    def min_max_value(self):
        if self.value_is_assigned:
            return self.value

        self.children = sorted(self.children, key = lambda x:x.min_max_value())

        if ((self.ply_depth % 2) == 0):
            print(self.children[-1][0])
            self.value = self.children[-1].value
        else:
            self.value = self.children[0].value

        self.value_is_assigned = True
        return self.value


    def generate_children(self, type):
        # If line or no line, generate all moving pieces
        for next_move_board in self.current_board.all_possible_moves(self.colour_as_int):
            colour = self.current_board.next_turn(self.colour_as_str)
            if colour == "white":
                self.colour_as_int = 1
            else:
                self.colour_as_int = 2
            
            self.children.append(search_tree_node(next_move_board, self.colour_as_int, (self.ply_depth + 1)))
        
        # If board has a line, generate pieces to remove
        if type == "line":
            for next_move_board in self.current_board.remove_colour_possibilities(self.colour_as_str):
                colour = self.current_board.next_turn(self.colour_as_str)
                if colour == "white":
                    self.colour_as_int = 1
                else:
                    self.colour_as_int = 2
            
                self.children.append(search_tree_node(next_move_board, self.colour_as_int, (self.ply_depth + 1)))




if __name__ == "__main__":
    from board_backend import current_board
    cb = current_board()
    cb.populate_board()
    
    st = search_tree_node(cb, 1)
    print(st.children[0])
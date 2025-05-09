class search_tree_node:
    def __init__(self, board_instance, colour, ply = 0, max_ply_depth = 5):
        self.children = []
        self.ply_depth = ply
        self.max_ply = max_ply_depth
        self.current_board = board_instance

        self.colour_as_int = colour
        if self.colour_as_int == 1:
            self.colour_as_str = "white"
        else:
            self.colour_as_str = "black"
        
        self.value_is_assigned = False

        
        # One colour has 2 pieces left
        if (self.current_board.white_pieces_on_board < 3) or (self.current_board.black_pieces_on_board < 3):
            # Branch complete
            self.value = 0

        # Game continues
        else:
            # Ply depth checker to break if ply depth is too large
            if self.ply_depth < self.max_ply:
                self.generate_children()

            if ((self.ply_depth % 2) == 0):
                self.value = -1
            else:
                self.value = 1
            self.value_is_assigned = True


    def min_max_value(self):
        if self.value_is_assigned:
            return self.value

        self.children = sorted(self.children, key = lambda x:x.min_max_value())

        if len(self.children) > 0:
            if ((self.ply_depth % 2) == 0):
                self.value = self.children[-1].value
            else:
                self.value = self.children[0].value
        else:
            self.value = -1

        self.value_is_assigned = True
        return self.value


    def generate_children(self):
        # Generate all moving pieces
        for next_move_board in self.current_board.all_possible_moves(self.colour_as_int):
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

    print("Starting board: " + cb.display())

    print()
    
    # Generate children
    st = search_tree_node(cb, 1)
    print("All children for first loop:")
    for child in st.children:
        print(child.current_board.display())

    # Sort boards
    st.min_max_value()
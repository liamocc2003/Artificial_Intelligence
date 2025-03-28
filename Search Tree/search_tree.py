class search_tree_node:
    def __init__(self, board_instance, colour, ply = 0):
        self.children = []
        self.ply_depth = ply
        self.current_board = board_instance
        self.colour = colour
        self.value_is_assigned = False

        # All pieces placed
        # No lines of 3 available, white goes first
        if self.current_board.board_state() == "3":
            self.generate_children()

        # Line of 3 found, if white continue as normal, if black change move to blacks turn
        else:
            # End of game
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


    def generate_children(self):
        ## Must fix all possible moves for new board generator
        for next_move_board in self.current_board.all_possible_moves(self.colour):
            self.children.append(search_tree_node(next_move_board, self.current_board.next_turn(self.colour), (self.ply_depth + 1)))


if __name__ == "__main__":
    search_tree_node()
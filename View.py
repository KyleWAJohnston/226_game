import Board


class View:

    def __init__(self, board):
        """
        Constructs the View object to display the board.
        :param board: [[str]] The Board to be displayed.
        """
        self.board = board

    def display_board(self):
        """
        Prints out the board in it's intended 2d format.
        :return: No return
        """
        board_len = len(self.board)
        line: str = ""

        for i in range(board_len):
            line += "\n"

            for j in range(board_len):
                if self.board[i][j].description is not None:
                    line += str(self.board[i][j].description) + "  "
                else:
                    line += "?  "

        return line

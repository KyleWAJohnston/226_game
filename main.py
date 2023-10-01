import View
import Board
import Treasure


treasure1: Treasure = Treasure.Treasure(1)

newBoard = Board.Board(1, 1, treasure1, 10)
newView = View.View(newBoard.board)

newView.display_board()

import View
import Board
import Treasure
import random


treasure1: Treasure = Treasure.Treasure(1)

newBoard = Board.Board(5, 10, treasure1, 10)

player_count: int = 0

for i in range(2):
    if newBoard.empty_spaces is None:
        raise ValueError("Error: No empty spaces on the board to create a player.")
    else:
        x, y = random.choice(newBoard.empty_spaces)
        newBoard.add_player(int(i + 1), x, y)
        newBoard.empty_spaces.remove((x, y))
        player_count += 1

newView = View.View(newBoard.board)
is_game_over: bool = False
turn: int = 0

while is_game_over is False:
    turn += 1
    current_player = player_count % turn

    newView.display_board()

    print(f"Player: ", current_player, newBoard.players[1])
    user_move = input("(U)p (L)eft (R)ight (D)own (Q)uit? ")

    newBoard.move_player(current_player, str(user_move))

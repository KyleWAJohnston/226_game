import View
import Board
import Treasure
import random


treasure1: Treasure = Treasure.Treasure(1)

newBoard = Board.Board(5, 10, treasure1, 10)

player_count: int = 0

# Adds players to the board at random tiles.
for i in range(2):
    if newBoard.empty_spaces is None:
        raise ValueError("No empty spaces on the board to create a player.")
    else:
        x, y = random.choice(newBoard.empty_spaces)
        newBoard.add_player(int(i + 1), x, y)
        newBoard.empty_spaces.remove((x, y))
        player_count += 1

# Creates the board view so the board can be drawn to the console.
newView = View.View(newBoard.board)

is_game_over: bool = False
turn: int = 0

# Basic gameplay logic, loops until the game is over. Handles moving of players and turns.
while is_game_over is False:
    # Automatically tracks which players turn it is.
    turn += 1
    current_player_name = ((turn - 1) % player_count) + 1

    # Find out if the game is over.
    if newBoard.treasure_tile_amount == 0:
        isGameOver = True
        break

    (current_player, (x, y)) = newBoard.players[current_player_name]

    # Draw the updated board again after every move.
    newView.display_board()

    # Print the current player whose turn it is, and the available move options.
    print(f"Player: ", current_player_name, " Score: ", current_player.score)

    user_move = input("(U)p (L)eft (R)ight (D)own (Q)uit? ")

    # Takes the players move choice and updates the board.
    newBoard.move_player(current_player_name, str(user_move))

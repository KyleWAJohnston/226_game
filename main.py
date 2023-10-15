import View
import Board
import Treasure
import random
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class Game:
    BUFF_SIZE = 1
    HOST = '127.0.0.1'
    PORT = 65432

    def __init__(self):
        self.treasure1: Treasure = Treasure.Treasure(1)
        self.newBoard = Board.Board(5, 10, self.treasure1, 10)
        self.player_count: int = 0
        self.newView = View.View(self.newBoard.board)
        self.is_game_over: bool = False
        self.turn: int = 0

    def start(self):
        # Adds players to the board at random tiles.
        for i in range(2):
            if self.newBoard.empty_spaces is None:
                raise ValueError("No empty spaces on the board to create a player.")
            else:
                x, y = random.choice(self.newBoard.empty_spaces)
                self.newBoard.add_player(int(i + 1), x, y)
                self.newBoard.empty_spaces.remove((x, y))
                self.player_count += 1
    
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((self.HOST, self.PORT))
            sock.listen(1)
            print('Server:', sock.getsockname())
    
            # Basic gameplay logic, loops until the game is over. Handles moving of players and self.turns.
            while self.is_game_over is False:
                sc, _ = sock.accept()
    
                # Receive the input from the client
                data = sc.recv(self.BUFF_SIZE)
    
                # Convert the data to a bit string
                number = int.from_bytes(data, byteorder="big")
                bit_string = '{0:b}'.format(number)
                print(bit_string)
    
                # Figure out which bits are set.
                for p in range(8):
                    print(f"Bit {p} is {1 if number & 2 ** p > 0 else 0}")
    
                # Automatically tracks which players self.turn it is.
                self.turn += 1
                current_player_name = ((self.turn - 1) % self.player_count) + 1
    
                # Find out if the game is over.
                if self.newBoard.treasure_tile_amount == 0:
                    self.is_game_over = True
                    break
    
                (current_player, (x, y)) = self.newBoard.players[current_player_name]
    
                # Draw the updated board again after every move.
                boardString: str = self.newView.display_board()
                print(boardString)
    
                # Print the current player whose self.turn it is, and the available move options.
                print(f"Player: ", current_player_name, " Score: ", current_player.score)
    
                user_move = input("(U)p (L)eft (R)ight (D)own (Q)uit? ")
    
                # Takes the players move choice and updates the board.
                self.newBoard.move_player(current_player_name, str(user_move))
    
                # Send the result to the client.
                sc.sendall(b"You sent: " + bit_string.encode() + b'\n')


g = Game()
g.start()

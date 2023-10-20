import struct
import View
import Board
import Treasure
import random
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class Game:
    BUFF_SIZE = 1
    HOST = ''
    PORT = 12345

    def __init__(self):
        self.treasure1: Treasure = Treasure.Treasure(1)
        self.newBoard = Board.Board(5, 10, self.treasure1, 10)
        self.player_count: int = 0
        self.newView = View.View(self.newBoard.board)
        self.is_game_over: bool = False
        self.turn: int = 0

    def start(self):
        PLAYER_ONE_BINARY = "00000100"
        PLAYER_TWO_BINARY = "00001000"

        # Adds players to the board at random tiles.
        for i in range(2):
            if self.newBoard.empty_spaces is None:
                raise ValueError("No empty spaces on the board to create a player.")
            else:
                x, y = random.choice(self.newBoard.empty_spaces)
                self.newBoard.add_player(int(i + 1), x, y)
                self.newBoard.empty_spaces.remove((x, y))
                self.player_count += 1
    
        with (socket(AF_INET, SOCK_STREAM) as sock):
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((self.HOST, self.PORT))
            sock.listen(1)
            print('Server:', sock.getsockname())
    
            # Basic gameplay logic, loops until the game is over. Handles moving of players and self.turns.
            while self.is_game_over is False:
                sc, _ = sock.accept()

                with sc:
                    # Receive the input from the client
                    data = sc.recv(self.BUFF_SIZE)

                    # Convert the data to a bit string
                    number = int.from_bytes(data, byteorder="big")
                    bit_string = '{0:b}'.format(number)
                    print("Bit string: " + bit_string)

                    # Translate the byte in number to a command and player numbers.
                    command_bits = self.get_movement_bits(bit_string)

                    if command_bits == "0010":
                        command = "U"
                    elif command_bits == "0100":
                        command = "L"
                    elif command_bits == "0110":
                        command = "R"
                    elif command_bits == "0011":
                        command = "D"
                    elif command_bits == "1000":
                        command = "Q"
                    elif command_bits == "1111":
                        board_string: str = self.newView.display_board()
                        print(board_string)
                        player1 = self.get_current_player(PLAYER_ONE_BINARY)
                        player2 = self.get_current_player(PLAYER_TWO_BINARY)
                        print("Score:\n" + "Player 1: " + str(player1.get_score()) + "\nPlayer 2: " +
                              str(player2.get_score()))

                        score1: int = player1.get_score()
                        score2: int = player2.get_score()

                        print(f"score 1: {score1}")

                        score_message1 = b'Player 1: ' + struct.pack('!H', score1)
                        score_message2 = b'Player 2: ' + struct.pack('!H', score2)

                        print(f"score 1 packed: {struct.pack('!H', score1)}")

                        sc.sendall(score_message1 + score_message2)
                        sc.sendall(board_string.encode())
                        continue
                    else:
                        command = "Unknown"

                    # Figure out which bits are set.
                    for p in range(8):
                        print(f"Bit {p} is {1 if number & 2 ** p > 0 else 0}")

                    # Automatically tracks which players self.turn it is.
                    # self.turn += 1
                    # current_player_name = ((self.turn - 1) % self.player_count) + 1

                    # Find out if the game is over.
                    if self.newBoard.treasure_tile_amount == 0:
                        self.is_game_over = True
                        break

                    # Takes the players move choice and updates the board.
                    current_player = self.get_current_player(bit_string)
                    self.newBoard.move_player(current_player.name, command)

                    # Draw the updated board again after every move.
                    board_string: str = self.newView.display_board()
                    print("Printing the board...\n" + board_string)

                    # Send the result to the client.
                    sc.sendall(b"You sent: " + bit_string.encode() + b'\n')

    def get_current_player(self, bit_string):
        player_bit_string = self.get_player_bits(bit_string)
        player_number = int(player_bit_string, 2)

        if player_number != 0:
            # Players are referenced by ints in the boards player list.
            (current_player, (x, y)) = self.newBoard.players[player_number]
        else:
            current_player = 0

        return current_player

    @staticmethod
    def fix_bit_length(bits):
        while len(bits) < 8:
            bits = "0" + bits

        return bits

    @staticmethod
    def get_movement_bits(bits):
        bits = Game.fix_bit_length(bits)
        movement_bits = str(bits)[0] + str(bits)[1] + str(bits)[2] + str(bits)[3]

        return movement_bits

    @staticmethod
    def get_player_bits(bits):
        bits = Game.fix_bit_length(bits)
        player_bits = str(bits)[4] + str(bits)[5]

        return player_bits


g = Game()
g.start()

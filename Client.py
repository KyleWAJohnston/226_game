import socket
from struct import pack, unpack
import pdb


class Client:
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 12345
        self.score = 0
        self.player_int = 0

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

    @staticmethod
    def check_input(userInput):
        """
        Check if user input is a proper command.
        :param userInput: Any str or chr to check.
        :return: Returns True is the input is a command, False if otherwise.
        """
        upperInput = userInput.upper()

        if upperInput in ["U", "D", "L", "R", "Q"]:
            return True
        else:
            return False

    def get_input(self):
        """
        Prompt for input until input is valid.
        :return: Returns the input.
        """
        isInputGood = False
        message = ""

        while not isInputGood:
            message = input("Enter U, D, L, R, or Q: ")
            isInputGood = self.check_input(message)

        return message

    @staticmethod
    def get_command_int(userCommand):
        upperCmd = userCommand.upper()

        if upperCmd == "U":
            return 32
        elif upperCmd == "L":
            return 64
        elif upperCmd == "R":
            return 96
        elif upperCmd == "D":
            return 48
        elif upperCmd == "Q":
            return 128
        else:
            return 15

    def receive_msg(self):
        header = self.client_socket.recv(2)
        message = b''

        if not header:
            self.client_socket.close()
        else:
            msg_length = unpack('!H', header)[0]

            while (len(message)) < msg_length:
                packet = self.client_socket.recv(msg_length - len(message))

                if not packet:
                    self.client_socket.close()

                message += packet

            return message

    def start(self):
        player_number = unpack('!B', self.receive_msg())[0]

        if player_number == 1:
            self.player_int = 4
        elif player_number == 2:
            self.player_int = 8
        else:
            print("Error receiving player info. Closing connection.")
            self.client_socket.close()

        while True:
            # Receive board and scores.
            self.client_socket.sendall(pack('!B', 240))

            raw_board = self.receive_msg()
            score1 = unpack('!H', raw_board[0:2])[0]
            score2 = unpack('!H', raw_board[2:4])[0]
            board = raw_board[4:].decode()

            print(board)
            
            # Get and check validity of user input.
            command = self.get_input()

            # Translate command into a bit_string.
            command_int = self.get_command_int(command) + self.player_int
            command_bits = pack('!B', command_int)

            # Send command.
            self.client_socket.sendall(command_bits)
            raw_scores = self.receive_msg()
            score1 = unpack('!H', raw_scores[0:2])[0]
            score2 = unpack('!H', raw_scores[2:4])[0]
            print(score1, score2)


# Run the client.
client = Client()
client.start()

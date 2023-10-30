import socket


class Client:
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 12345
        self.score = 0
        self.player_bits = '0000'

    @staticmethod
    def check_input(userInput):
        """
        Check if user input is a proper command.
        :param userInput: Any str or chr to check.
        :return: Returns True is the input is a command, False if otherwise.
        """
        if userInput in ["U", "D", "L", "R", "Q"]:
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
    def get_command_bits(userCommand):
        if userCommand == "U":
            return "0010"
        elif userCommand == "L":
            return "0100"
        elif userCommand == "R":
            return "0110"
        elif userCommand == "D":
            return "0011"
        elif userCommand == "Q":
            return "1000"
        else:
            return "1111"

    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((self.server_ip, self.server_port))

        player_bits = client_socket.recv(1)

        while True:
            # Open connection and receive data.
            data_size = client_socket.recv(1)
            data = client_socket.recv(data_size)
            if not data:
                print("No data from server.")
                break
            else:
                print("Received data from server: " + data.decode('utf-8') + "\n")

            # Get and check validity of user input.
            command = self.get_input()

            # Translate command into a bit_string.
            command_bits = self.get_command_bits(command)
            send_bits = command_bits + player_bits

            # Send command.
            client_socket.sendall(send_bits.encode('utf-8'))

            # Receive scores. I don't know why we're sending the size when we know what it will be...
            data_size = client_socket.recv(2)
            client_socket.recv(data_size)



# Run the client.
client = Client()
client.start()

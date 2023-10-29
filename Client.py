import socket


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


def get_input():
    """
    Prompt for input until input is valid.
    :return: Returns the input.
    """
    isInputGood = False
    message = ""

    while not isInputGood:
        message = input("Enter U, D, L, R, or Q: ")
        isInputGood = check_input(message)

    return message


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


server_ip = '127.0.0.1'
server_port = 12345
score = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))
player_bits = client_socket.recv(1)

while True:
    # Open connection and receive data.
    data = client_socket.recv(1)
    if not data:
        print("No data from server.")
        break
    else:
        print("Connected to server.\n")

    # Get and check validity of user input.
    print("Received data from server: " + data.decode('utf-8') + "\n")
    command = get_input()

    # Translate command into a bit_string.
    command_bits = get_command_bits(command)
    send_bits = command_bits + player_bits

    # Send command.
    client_socket.sendall(send_bits.encode('utf-8'))

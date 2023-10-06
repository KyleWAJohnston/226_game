import Treasure
import Tile
import Player
import random


class Board:

    def __init__(self, min_val: int, max_val: int, t: Treasure, n: int):
        """
        Constructs the Board as a 2d array.
        :param min_val: int The minimum value of the Treasure.
        :param max_val: int The maximum value of the Treasure.
        :param t: Treasure The Treasure object used to populate the Tiles with treasure.
        :param n: int The size of the board will be n X n.
        """
        self.max_players = n
        self.players: Player = {}
        self.n = n
        self.player_count: int = 0

        # Tile instances
        self.default: Tile = Tile.Tile()
        treasure_tile1: Tile = Tile.Tile(t.description, t)
        self.player_tiles: Tile = {}

        # Create the 2d board filled with default Tiles.
        self.board = [[self.default for x in range(n)] for x in range(n)]

        # Create a tuple of empty spaces.
        self.empty_spaces = [(x, y) for x in range(n) for y in range(n)]

        # count: int = 0
        for i in range(5):
            x, y = random.choice(self.empty_spaces)
            val = random.randint(min_val, max_val)
            treasure_tile1.value = val
            self.board[x][y] = treasure_tile1
            self.empty_spaces.remove((x, y))

    def add_player(self, name, x: int, y: int):
        self.player_count += 1
        player_desc = self.player_count

        if self.max_players > self.player_count:
            new_player = Player.Player(name)
            self.players[self.player_count] = (new_player, (x, y))

            new_player_tile: Tile = Tile.Tile(player_desc)
            new_player_tile.add_player(new_player)
            self.player_tiles[player_desc] = new_player_tile

            self.board[x][y] = new_player_tile
        else:
            print("Error: Maximum amount of players has already been reached for this board size.")

    def move_player(self, name, direction):
        """
        Moves the players position on the board according to the given input.
        :param name: The player being moved.
        :param direction: The direction the player is being moved.
        """
        if name not in self.players:
            raise ValueError("Error: No player by that name.")

        current_player, (current_x, current_y) = self.players[name]

        new_x: int = 0
        new_y: int = 0
        was_pos_updated: bool = True

        match direction.upper():
            case "U" | "UP":
                if current_x == 0:
                    raise ValueError("Player.py cannot go up.")
                else:
                    new_x = current_x - 1
                    new_y = current_y
            case "D" | "DOWN":
                if current_x == self.n - 1:
                    raise ValueError("Player.py cannot go down.")
                else:
                    new_x = current_x + 1
                    new_y = current_y
            case "L" | "LEFT":
                if current_y == 0:
                    raise ValueError("Player.py cannot go left.")
                else:
                    new_y = current_y - 1
                    new_x = current_x
            case "R" | "RIGHT":
                if current_y == self.n - 1:
                    raise ValueError("Player.py cannot go right.")
                else:
                    new_y = current_y + 1
                    new_x = current_x
            case other:
                raise ValueError("Invalid input. Only enter either U, L, R, D, or Q.")
                was_pos_updated = False

        if was_pos_updated:
            new_position = (current_player, (new_x, new_y))
            self.players[name] = new_position
            self.board[current_x][current_y] = self.default
            self.board[new_x][new_y] = self.player_tiles[current_player.name]

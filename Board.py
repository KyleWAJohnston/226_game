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
        self.min_val = min_val
        self.max_val = max_val
        self.max_players = n
        self.players: Player = {}
        self.t = t
        self.n = n
        self.player_count: int = 0
        self.treasure_tile_amount = 0

        # Treasure instances
        self.treasures = {}

        # Tile instances
        self.default: Tile = Tile.Tile()
        self.player_tiles: Tile = {}

        # Create the 2d board filled with default Tiles.
        self.board = [[self.default for x in range(n)] for x in range(n)]

        # Create a tuple of empty spaces.
        self.empty_spaces = [(x, y) for x in range(n) for y in range(n)]

        treasure_tile: Treasure = Tile.Tile()
        for i in range(5):
            x, y = random.choice(self.empty_spaces)
            val = random.randint(min_val, max_val)

            self.treasures[i] = Treasure.Treasure(val)
            treasure_tile = Tile.Tile(self.treasures[i].description, self.treasures[i])

            self.treasure_tile_amount += 1

            self.board[x][y] = treasure_tile
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

        while True:
            new_x: int = 0
            new_y: int = 0
            was_pos_updated: bool = True

            match direction.upper():
                case "U" | "UP":
                    # if current_x == 0:
                    #     raise ValueError("Player cannot go up.")
                    # else:
                    new_x = current_x - 1
                    new_y = current_y
                case "D" | "DOWN":
                    # if current_x == self.n - 1:
                    #     raise ValueError("Player cannot go down.")
                    # else:
                    new_x = current_x + 1
                    new_y = current_y
                case "L" | "LEFT":
                    # if current_y == 0:
                    #     raise ValueError("Player cannot go left.")
                    # else:
                    new_y = current_y - 1
                    new_x = current_x
                case "R" | "RIGHT":
                    # if current_y == self.n - 1:
                    #     raise ValueError("Player cannot go right.")
                    # else:
                    new_y = current_y + 1
                    new_x = current_x
                case "Q" | "QUIT":
                    print("Game closed.")
                    was_pos_updated = False
                    quit()
                case other:
                    raise ValueError("Invalid input. Only enter either U, L, R, D, or Q.")
                    was_pos_updated = False

            if was_pos_updated:
                new_position = (current_player, (new_x, new_y))
                self.players[name] = new_position

                if self.board[new_x][new_y].player is not None or new_x > self.n - 1 or new_x < 0 or new_y > self.n - 1 or new_y < 0:
                    print("Already a player there or at the edge of the board, try again.")
                    direction = input("(U)p (L)eft (R)ight (D)own (Q)uit? ")
                else:
                    if self.board[new_x][new_y].instance is not None:
                        current_tile: Tile = self.board[new_x][new_y].instance
                        treasure_value: int = current_tile.value
                        current_player.update_score(treasure_value)
                        self.treasure_tile_amount -= 1

                        if self.treasure_tile_amount == 0:
                            print("\nGame Over")
                            print("Final score: ")

                            for i in self.players:
                                (current_player, (x, y)) = self.players[i]
                                print("Player " + str(current_player.name) + ": " + str(current_player.score))

                    self.board[current_x][current_y] = self.default
                    self.board[new_x][new_y] = self.player_tiles[current_player.name]
                    break

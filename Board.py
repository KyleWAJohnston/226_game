import Treasure
import Tile
import random


class Board:

    def __init__(self, min_val: int, max_val: int, t: Treasure, n: int):
        """
        Constructs the Board as a 2d array.
        :param min_val:
        :param max_val:
        :param t: Treasure The Treasure object used to populate the Tiles with treasure.
        :param n: int The size of the board will be n X n.
        """
        # Tile instances
        default: Tile = Tile.Tile()
        treasure_tile1: Tile = Tile.Tile(t.description, t)

        # Create the 2d board filled with default Tiles.
        self.board = [[default for x in range(n)] for x in range(n)]

        # Create a tuple of empty spaces.
        self.empty_spaces = [(x, y) for x in range(n) for y in range(n)]

        # DEBUGGING CODE
        print(self.board.__len__())

        # count: int = 0
        for i in range(5):
            x, y = random.choice(self.empty_spaces)
            val = random.randint(5, 10)
            treasure_tile1.value = val
            self.board[x][y] = treasure_tile1

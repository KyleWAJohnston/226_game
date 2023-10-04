import Treasure
import Player


class Tile:

    def __init__(self, desc: chr = '.', instance: Treasure = None):
        """
        Constructs a Tile which is used to populate the Board.
        :param desc: chr The symbol used to represent the Tile. Defaults to '.'.
        :param instance: Treasure The Treasure within the Tile. Defaults to none.
        """
        if instance is not None:
            self.description: chr = instance.description
            self.instance: Treasure = instance
        else:
            self.description: chr = desc
            self.instance = instance

        self.player = None

    def add_player(self, player: Player):
        self.player = player

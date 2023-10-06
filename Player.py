
class Player:

    def __init__(self, name):
        """
        Creates a player object.
        :param name: The name of the player.
        """
        self.name = name
        self.score = 0

    def update_score(self, value: int):
        self.score += value

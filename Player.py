
class Player:

    def __init__(self, name):
        """
        Creates a player object.
        :param name: The name of the player.
        """
        self.name = name
        self.score: int = 0

    def get_score(self):
        return self.score

    def update_score(self, value: int):
        self.score += value

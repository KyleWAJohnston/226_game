from django.test import TestCase
from django.urls import reverse
from .models import Board, Player


# Create your tests here.
class BoardTestsCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Board.create_board()
        Board.populate_treasure()
        Board.populate_players()

    def test_amount_of_tiles(self):
        tiles = Board.objects.all()
        self.assertEqual(tiles.count(), 100)

    def test_amount_of_treasures(self):
        treasures = Board.objects.filter(value__gte=1)
        self.assertEqual(treasures.count(), 5)

    def test_amount_of_players(self):
        players = Board.objects.filter(value=-1)
        self.assertEquals(players.count(), 2)

    def test_bottom_border(self):
        player1 = Player.objects.get(tag=1)
        player2 = Player.objects.get(tag=2)

        # Move player 2 out of the way.
        player2.col = 0
        player2.row = 0
        player2.save()

        # Move the player to the bottom.
        player2.col = 9
        player1.row = 9
        player1.save()

        # After player is at the bottom, move the player down again. Position should not change.
        self.client.post(reverse('move_player', args=(player1.tag, 'down')))
        player1.refresh_from_db()

        # Assert that the player is at, not beyond, the bottom border.
        self.assertEqual(player1.row, 9)

    def test_top_border(self):
        player1 = Player.objects.get(tag=1)
        player2 = Player.objects.get(tag=2)

        # Move player 2 out of the way.
        player2.col = 0
        player2.row = 9
        player2.save()

        # Move the player to the bottom.
        player1.col = 9
        player1.row = 0
        player1.save()

        # After player is at the top, move the player up again. Position should not change.
        self.client.post(reverse('move_player', args=(player1.tag, 'up')))
        player1.refresh_from_db()

        # Assert that the player is at, not beyond, the top border.
        self.assertEqual(player1.row, 0)

    def test_left_border(self):
        player1 = Player.objects.get(tag=1)
        player2 = Player.objects.get(tag=2)

        # Move player 2 out of the way.
        player2.col = 9
        player2.row = 0
        player2.save()

        # Move the player to the left.
        player1.col = 0
        player1.row = 9
        player1.save()

        # After player is at the left, move the player left again. Position should not change.
        self.client.post(reverse('move_player', args=(player1.tag, 'left')))
        player1.refresh_from_db()

        # Assert that the player is at, not beyond, the left border.
        self.assertEqual(player1.col, 0)

    def test_right_border(self):
        player1 = Player.objects.get(tag=1)
        player2 = Player.objects.get(tag=2)

        # Move player 2 out of the way.
        player2.col = 0
        player2.row = 0
        player2.save()

        # Move the player to the right.
        player1.col = 9
        player1.row = 9
        player1.save()

        # After player is at the right, move the player right again. Position should not change.
        self.client.post(reverse('move_player', args=(player1.tag, 'right')))
        player1.refresh_from_db()

        # Assert that the player is at, not beyond, the right border.
        self.assertEqual(player1.row, 0)

    def test_treasure_pickup(self):
        player1 = Player.objects.get(tag=1)
        player2 = Player.objects.get(tag=2)

        # Position the players.
        player2.col = 9
        player2.row = 9
        player2.save()
        player1.col = 0
        player1.row = 0
        player1.save()

        # Set a treasure bellow player 1.
        tile0x1 = Board.objects.get(col=0, row=1)
        tile0x1.value = 3
        tile0x1.save()

        # Move player 1 into the treasure tile.
        self.client.post(reverse('move_player', args=(player1.tag, 'down')))
        player1.refresh_from_db()

        # Assert that player 1 has a score of 3.
        self.assertEqual(player1.score, 3)

    def test_player_collision(self):
        player1 = Player.objects.get(tag=1)
        player2 = Player.objects.get(tag=2)
        top_right_tile = Board.objects.get(row=0, col=0)

        # Position the players next to each-other.
        # player2.col = 0
        # player2.row = 0
        # player2.save()
        # top_right_tile.value = -1
        player1.col = 0
        player1.row = 1
        player1.save()
        
        while player2.col is not 0 and player2.row is not 0:
            self.client.post(reverse('move_player', args=(player2.tag, "up")))
            self.client.post(reverse('move_player', args=(player2.tag, "left")))

        # Attempt to move player 1 into player 2.
        self.client.post(reverse('move_player', args=(player1.tag, "up")))
        player1.refresh_from_db()

        # Assert that player 1 was not able to move and is in the original position.
        self.assertEqual(player1.row, 1)

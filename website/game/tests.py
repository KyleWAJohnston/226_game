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

        # Move the player to the bottom.
        while player1.row < 9:
            self.client.post(reverse('move_player', args=(player1.tag, 'down')))
            player1.refresh_from_db()

        # After player is at the bottom, move the player down again. Position should not change.
        self.client.post(reverse('move_player', args=(player1.tag, 'down')))
        player1.regresh_from_db()

        # Assert that the player is at, not beyond, the bottom border.
        self.assertEqual(player1.row, 9)

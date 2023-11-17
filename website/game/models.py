from django.db import models
import random


# Create your models here.
class Board(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    label = models.CharField(max_length=1)
    value = models.IntegerField()

    @classmethod
    def create_board(cls):
        Player.objects.all().delete()
        cls.objects.all().delete()

        for row in range(10):
            for col in range(10):
                cls.objects.create(row=row, col=col, label='.', value=0)

    @classmethod
    def populate_treasure(cls):
        empty_tiles = list(cls.objects.filter(value=0))
        random.shuffle(empty_tiles)

        for tile in empty_tiles[:5]:
            tile.value = random.randint(1, 10)
            tile.label = '$'
            tile.save()

    @classmethod
    def populate_players(cls):
        empty_tiles = list(cls.objects.filter(value=0))
        random.shuffle(empty_tiles)
        player_count = 0
        num_players = 2

        for tile in empty_tiles[:num_players]:
            player_count += 1
            Player.objects.create(tag=str(player_count), row=tile.row, col=tile.col, score=0)
            tile.value = -1
            tile.label = str(player_count)
            tile.save()


class Player(models.Model):
    tag = models.CharField(max_length=1)
    row = models.IntegerField()
    col = models.IntegerField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.tag} @({self.row}, {self.col})'

from Treasure import Treasure
from Tile import Tile
from Board import Board
from View import View
from Player import Player


def test_treasure():
    t1 = Treasure(10)
    t2 = Treasure(20, '%')

    assert t1.value == 10
    assert t1.description == '$'
    assert t2.value == 20
    assert t2.description == '%'


def test_tile():
    treasure1 = Treasure(5)
    tile1 = Tile()
    tile2 = Tile('*')
    tile3 = Tile(instance=treasure1)

    assert tile1.description == '.'
    assert tile1.instance is None
    assert tile2.description == '*'
    assert tile2.instance is None
    assert tile3.description == '$'
    assert tile3.instance == treasure1


def test_board():
    treasure1 = Treasure(4)
    b1 = Board(1, 5, treasure1, 10)
    b1.add_player("Board Test Player", 9, 3)

    assert b1.min_val == 1
    assert b1.max_val == 5
    assert b1.t == treasure1
    assert b1.n == 10
    assert b1.player_count == 1


def test_view():
    treasure1 = Treasure(9)
    b1 = Board(3, 9, treasure1, 15)
    v1 = View(b1)

    assert v1.board == b1


def test_player():
    p1 = Player("Player 1")
    p1.update_score(5)

    assert p1.name == "Player 1"
    assert p1.score == 5

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Board, Player


def create_game(request):
    # Method calls.
    Board.create_board()
    Board.populate_treasure()
    Board.populate_players()

    return render(request, 'game/create_game.html')


def choose_player(request):
    # Get the tiles, order the tiles.
    board_tiles = Board.objects.all().order_by('row', 'col')
    players = Player.objects.all().order_by('tag')

    # Organize board tiles into a grid.
    grid_size = 10
    grid = [list(board_tiles[i:i + grid_size]) for i in range(0, len(board_tiles), grid_size)]

    # Player tags.
    num_players = 2
    player_tag = [str(i + 1) for i in range(num_players)]

    context = {
        'player_tag': player_tag,
        'grid': grid
    }

    return render(request, 'game/choose_player.html', context)


def play_game(request, player_tag):
    # Get the tiles, order the tiles.
    board_tiles = Board.objects.all().order_by('row', 'col')

    # Organize board tiles into a grid.
    grid_size = 10
    grid = [list(board_tiles[i:i + grid_size]) for i in range(0, len(board_tiles), grid_size)]

    # Get players.
    player1 = Player.objects.get(tag='1')
    player2 = Player.objects.get(tag='2')

    context = {
        'player_tag': player_tag,
        'grid': grid,
        'player1_score': player1.score,
        'player2_score': player2.score
    }

    return render(request, 'game/play_game.html', context)


def move_player(request, player_tag, direction):
    # Get data from Player and Board.
    player = Player.objects.get(tag=player_tag)

    # Set row and col.
    new_row = player.row
    new_col = player.col

    # Interpret direction and update player position.
    if direction == 'up':
        new_row -= 1
    elif direction == 'down':
        new_row += 1
    elif direction == 'left':
        new_col -= 1
    elif direction == 'right':
        new_col += 1

    # Validate and set position.
    if 0 <= new_row < 10 and 0 <= new_col < 10:
        current_tile = Board.objects.get(row=player.row, col=player.col)
        new_tile = Board.objects.get(row=new_row, col=new_col)

        if new_tile and new_tile.value != -1:
            player.score += new_tile.value

            current_tile.label = '.'
            current_tile.value = 0
            current_tile.save()

            new_tile.label = str(player_tag)
            new_tile.value = -1
            new_tile.save()

            player.row = new_row
            player.col = new_col
            player.save()

    return HttpResponseRedirect(reverse('play_game', args=player_tag,))

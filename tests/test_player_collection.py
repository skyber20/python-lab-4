import pytest

from src.collections.player_collection import PlayerCollection
from src.entities.player import Player
from src.entities.chip import Chip
from src.exceptions import PlayerNotFound


def test_player_collection_creation():
    pc = PlayerCollection()
    assert len(pc) == 0
    assert list(pc) == []

    pc = PlayerCollection()
    player = Player("Вася", 100, Chip(50))
    pc.add(player)

    assert len(pc) == 1
    assert pc[0] == player
    assert player in pc

    multy_players = [f'Игрок_{i}' for i in range(10)]
    pc = PlayerCollection()

    for i in range(len(multy_players)):
        player = Player(multy_players[i], 10 * i, Chip(50 * i))
        pc.add(player)

        assert len(pc) == i + 1
        assert player in pc

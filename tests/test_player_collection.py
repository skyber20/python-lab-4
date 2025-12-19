import pytest

from src._collections.player_collection import PlayerCollection
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


def test_remove_player():
    pc = PlayerCollection()
    player1 = Player("Вася", 100, Chip(50))
    pc.add(player1)

    assert len(pc) == 1
    assert player1 in pc

    pc.remove_player(player1)
    assert len(pc) == 0
    assert player1 not in pc

    with pytest.raises(PlayerNotFound):
        pc.remove_player(player1)


def test_remove_player_by_name():
    pc = PlayerCollection()
    player1 = Player("Вася", 100, Chip(50))
    pc.add(player1)

    assert len(pc) == 1
    assert player1 in pc

    pc.remove_player_by_name(player1.name)
    assert len(pc) == 0
    assert player1 not in pc

    with pytest.raises(PlayerNotFound):
        pc.remove_player_by_name(player1.name)


def test_clear_players():
    pc = PlayerCollection()
    player1 = Player("Вася", 100, Chip(50))
    player2 = Player('Art', 1000, Chip(100))
    pc.add(player1)
    pc.add(player2)

    assert len(pc) == 2
    assert player1 in pc
    assert player2 in pc

    pc.clear_players()
    assert len(pc) == 0


def test_get_names():
    pc = PlayerCollection()
    player1 = Player("Вася", 100, Chip(50))
    player2 = Player('Art', 1000, Chip(100))
    pc.add(player1)
    pc.add(player2)

    assert pc.get_names() == [player1.name, player2.name]


def test_find_by_name():
    pc = PlayerCollection()
    player1 = Player("Анна", 100, Chip(20))
    player2 = Player("Борис", 200, Chip(30))

    pc.add(player1)
    pc.add(player2)

    found = pc.find_by_name("Анна")
    assert found == player1

    found = pc.find_by_name("Борис")
    assert found == player2

    found = pc.find_by_name("Alex")
    assert found is None


def test_rich_poor_player():
    """Тест поиска самого богатого и самого бедного игроков"""
    pc = PlayerCollection()

    seniour = Player("Сеньор", 1000, Chip(500))  # Всего: 1500
    middle = Player("Миддл", 500, Chip(200))  # Всего: 700
    juniour = Player("Безработный", 100, Chip(50))  # Всего: 150

    pc.add(seniour)
    pc.add(middle)
    pc.add(juniour)

    poor = pc.poor_player()
    assert poor == juniour

    rich = pc.rich_player()
    assert rich == seniour


def test_add_collection():
    pc1 = PlayerCollection()
    pc2 = PlayerCollection()

    players1 = [Player('Art', 100, Chip(50)), Player('Fedya', 500, Chip(20))]

    for player in players1:
        pc1.add(player)

    assert pc1.get_names() == [p.name for p in players1]

    players2 = [Player('Poor', 1, Chip(0)), Player('Seniour', 10000, Chip(100)), Player('smbd', 20, Chip(50))]

    for player in players2:
        pc2.add(player)

    pc1 += pc2

    assert pc1.get_names() == [p.name for p in players1 + players2]


def test_index():
    pc = PlayerCollection()
    players = [Player(f"Игрок{i}", i * 100, Chip(i * 10)) for i in range(5)]

    for p in players:
        pc.add(p)

    index = pc[2]
    assert index == players[2]

    with pytest.raises(IndexError):
        index = pc[10]


def test_collection_slice():
    """Тест среза коллекции"""
    pc = PlayerCollection()
    players = [Player(f"Игрок{i}", i * 100, Chip(i * 10)) for i in range(5)]

    for p in players:
        pc.add(p)

    sliced = pc[1:4]
    assert len(sliced) == 3
    assert sliced[0] == players[1]
    assert sliced[1] == players[2]
    assert sliced[2] == players[3]

    sliced_step = pc[0:5:2]
    assert len(sliced_step) == 3
    assert sliced_step[0] == players[0]
    assert sliced_step[1] == players[2]
    assert sliced_step[2] == players[4]

    sliced = pc[10:20]  # Вне диапазона
    assert len(sliced) == 0


def test_collection_contains():
    """Тест оператора in"""
    pc = PlayerCollection()
    player1 = Player("Вася", 100, Chip(50))
    player2 = Player("Петя", 200, Chip(30))

    pc.add(player1)

    assert player1 in pc
    assert player2 not in pc

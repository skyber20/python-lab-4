import pytest

from src._collections.casino_balance import CasinoBalance
from src.entities.player import Player
from src.entities.chip import Chip
from src._collections.player_collection import PlayerCollection
from src.exceptions import PlayerNotFound


def test_casino_balance_creation():
    cb = CasinoBalance()
    p1 = Player('Art', 1000, Chip(100))
    p2 = Player('Max', 150, Chip(100))

    cb.add_player(p1)
    cb[p2.name] = p2.balance

    assert len(cb) == 2
    assert cb['Art'] == 1000
    assert cb['Max'] == 150


def test_set_item_update():
    """Тест обновления существующего баланса"""
    cb = CasinoBalance()
    cb["Вася"] = 100
    cb["Вася"] = 150

    assert cb["Вася"] == 150
    assert len(cb) == 1


def test_get_item_not_found():
    """Тест получения несуществующего баланса"""
    cb = CasinoBalance()
    cb["Вася"] = 100

    with pytest.raises(PlayerNotFound):
        _ = cb["Петя"]


def test_del_item():
    """Тест удаления баланса"""
    cb = CasinoBalance()
    cb["Вася"] = 100
    cb["Петя"] = 200

    assert len(cb) == 2
    del cb["Вася"]

    assert len(cb) == 1
    with pytest.raises(PlayerNotFound):
        _ = cb["Вася"]


def test_contains():
    """Тест оператора in"""
    cb = CasinoBalance()
    cb["Вася"] = 100

    assert "Вася" in cb
    assert "Петя" not in cb


def test_push_players_overwrite():
    """Тест пуша"""
    cb = CasinoBalance()
    p1 = Player('Art', 1000, Chip(100))
    p2 = Player('Max', 150, Chip(100))

    assert len(cb) == 0

    players = PlayerCollection()
    players.add(p1)
    players.add(p2)

    cb.push_players(players)
    assert len(cb) == 2
    assert cb['Art'] == 1000
    assert cb['Max'] == 150

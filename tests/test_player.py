import pytest

from src.entities.player import Player
from src.entities.chip import Chip
from src.exceptions import NotEnoughMoney, NotEnoughChips


def test_player_creation():
    """Тест создания игрока"""
    player = Player("Вася", 100, Chip(50))
    assert player.name == "Вася"
    assert player.balance == 100
    assert player.amount_chips.amount == 50


def test_player_update_balance():
    player = Player('Игрок', 100, Chip(50))

    player.update_balance(20)
    assert player.balance == 120

    player.update_balance(-20)
    assert player.balance == 100

    with pytest.raises(TypeError):
        player.update_balance('хай')


def test_player_is_bankrupt():
    """Тест проверки банкротства"""
    # Банкрот
    player1 = Player("Банкрот", 0, Chip(0))
    assert player1.is_bankrupt is True

    # Не банкрот (есть деньги)
    player2 = Player("Не банкрот", 10, Chip(0))
    assert player2.is_bankrupt is False

    # Не банкрот (есть фишки)
    player3 = Player("Не банкрот", 0, Chip(10))
    assert player3.is_bankrupt is False


def test_player_buy_chips():
    """Тест покупки фишек с достаточным количеством денег и недостаточным"""
    player = Player("Бедняк", 20, Chip(0))

    player.buy_chips(15)
    assert player.amount_chips.amount == 15
    assert player.balance == 5

    with pytest.raises(NotEnoughMoney):
        player.buy_chips(50)


def test_player_sell_chips():
    """Тест продажи фишек"""
    player = Player("Игрок", 100, Chip(50))
    player.sell_chips(30)

    assert player.balance == 130
    assert player.amount_chips.amount == 20

    with pytest.raises(NotEnoughChips):
        player.sell_chips(50)


def test_player_equals():
    player1 = Player('Art', 100, Chip(50))
    player2 = Player('Федя', 50, Chip(60))
    player3 = Player('Art', 100, Chip(50))

    assert player1 != player2
    assert player1 == player3

    with pytest.raises(TypeError):
        assert player1 == 'Казик'

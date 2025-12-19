import pytest

from src._collections.goose_collection import GooseCollection
from src._collections.player_collection import PlayerCollection
from src.casik import Casino
from src.entities.player import Player
from src.entities.chip import Chip
from src.entities.goose import Goose, WarGoose, HonkGoose
from unittest.mock import patch


def test_casino_creation():
    casino = Casino()
    p1 = Player('Art', 1000, Chip(50))
    g1 = Goose('Android_goose', 8)

    casino.register_player(p1)
    casino.register_goose(g1)

    assert casino.name == "Гусиный казик"
    assert len(casino.players) == 1
    assert p1.name in casino.balances
    assert len(casino.geese) == 1

    pc = PlayerCollection()
    pc.add(p1)
    gc = GooseCollection()
    gc.add(g1)

    casino2 = Casino(pc, gc)
    assert len(casino2.players) == 1
    assert len(casino2.geese) == 1


def test_player_defeated():
    casino = Casino()
    p1 = Player('Art', 1000, Chip(50))

    casino.register_player(p1)
    assert len(casino.players) == 1

    casino.player_defeated(p1)
    assert len(casino.players) == 0


def test_register_player_bankrupt():
    """Тест регистрации банкрота"""
    casino = Casino()
    player = Player("Банкрот", 0, Chip(0))  # Банкрот

    casino.register_player(player)

    assert len(casino.players) == 0


def test_random_player_empty():
    """Тест выбора случайного игрока из пустой коллекции"""
    casino = Casino()
    player = casino.random_player()
    assert player is None

def test_random_player_with_players():
    """Тест выбора случайного игрока"""
    casino = Casino()
    player1 = Player("Вася", 100, Chip(50))
    player2 = Player("Петя", 200, Chip(30))

    casino.register_player(player1)
    casino.register_player(player2)

    with patch('random.choice') as mock_choice:
        mock_choice.return_value = player1
        result = casino.random_player()
        assert result == player1


def test_random_goose_empty():
    """Тест выбора случайного гуся из пустой коллекции"""
    casino = Casino()
    goose = casino.random_goose()
    assert goose is None


def test_random_goose_with_type():
    """Тест выбора случайного гуся определенного типа"""
    casino = Casino()
    war_goose = WarGoose("Воин", 8)
    honk_goose = HonkGoose("Крикун", 6)

    casino.register_goose(war_goose)
    casino.register_goose(honk_goose)

    with patch('random.choice') as mock_choice:
        mock_choice.return_value = war_goose
        result = casino.random_goose(WarGoose)
        assert result == war_goose



def test_plus_money_success():
    """Тест успешного пополнения баланса из фишек"""
    casino = Casino()
    player = Player("Игрок", -50, Chip(100))
    casino.register_player(player)

    result = casino.plus_money(player, 50)

    assert result is True
    assert player.balance == 0
    assert player.amount_chips.amount == 50


def test_plus_money_not_enough_chips():
    """Тест пополнения когда не хватает фишек"""
    casino = Casino()
    player = Player("Игрок", -100, Chip(50))
    casino.register_player(player)

    result = casino.plus_money(player, 100)

    # Игрок остается, но баланс не пополняется
    assert result is True
    assert player.balance == -100
    assert player.amount_chips.amount == 50


def test_plus_money_no_chips():
    """Тест пополнения когда нет фишек"""
    casino = Casino()
    player = Player("Игрок", -100, Chip(1))
    casino.register_player(player)
    player.amount_chips = Chip(0)

    result = casino.plus_money(player, 100)

    # Игрок должен быть удален
    assert result == False
    assert player.name not in casino.balances
    assert player not in casino.players


def test_perform_attack_with_players_and_geese():
    """Тест ивента атаки гуся"""
    casino = Casino()
    player = Player("Игрок", 100, Chip(50))
    war_goose = WarGoose("Воин", 8)

    casino.register_player(player)
    casino.register_goose(war_goose)

    initial_balance = player.balance

    # Фиксируем рандом для предсказуемости
    with patch('random.choice') as mock_choice:
        mock_choice.side_effect = [war_goose, player]

        with patch('random.randint') as mock_randint:
            mock_randint.return_value = 10  # damage = 8 * 10 = 80
            casino.perform_attack()

    # Проверяем что баланс уменьшился
    assert player.balance == initial_balance - 80
    assert casino.balances[player.name] == player.balance


def test_perform_honk():
    """Тест ивента крика гуся"""
    casino = Casino()
    player = Player("Игрок", 100, Chip(50))
    honk_goose = HonkGoose("Крикун", 7)

    casino.register_player(player)
    casino.register_goose(honk_goose)

    initial_balance = player.balance

    with patch('random.choice') as mock_choice:
        mock_choice.side_effect = [honk_goose, player, '+']

        with patch('random.randint') as mock_randint:
            mock_randint.return_value = 10  # effect_power = 7 * 10 = 70
            casino.perform_honk()

    # Баланс должен измениться
    assert player.balance == initial_balance + 70
    assert casino.balances[player.name] == player.balance


def test_perform_bet():
    """Тест ивента ставки"""
    casino = Casino()
    player = Player("Игрок", 100, Chip(50))
    casino.register_player(player)

    initial_balance = player.balance

    with patch('random.choice') as mock_choice:
        mock_choice.side_effect = [player, True]

        with patch('random.randint') as mock_randint:
            # bet_amount = 50, потом результат ставки (выиграет)
            mock_randint.side_effect = [50, 0]
            casino.perform_bet()

    assert player.balance == initial_balance + 50
    assert casino.balances[player.name] == player.balance


def test_perform_bet_with_chips():
    """Тест ставки когда есть только фишки"""
    casino = Casino()
    player = Player("Игрок", 0, Chip(100))  # Нет денег, есть фишки
    casino.register_player(player)

    # Мокаем рандом для пополнения баланса
    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [50, 30]

        with patch('random.choice') as mock_choice:
            # проиграет
            mock_choice.side_effect = [player, False]
            casino.perform_bet()

    assert player.balance == 20
    assert casino.balances[player.name] == player.balance
#
#
def test_perform_steal():
    """Тест ивента Робин Гусь"""
    casino = Casino()

    rich_player = Player("Богач", 1000, Chip(500))
    poor_player = Player("Бедняк", 10, Chip(5))
    goose = Goose("Робин", 5)

    casino.register_player(rich_player)
    casino.register_player(poor_player)
    casino.register_goose(goose)

    initial_rich_chips = rich_player.amount_chips.amount
    initial_poor_chips = poor_player.amount_chips.amount

    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 100
        casino.perform_steal()

    assert rich_player.amount_chips.amount == initial_rich_chips + 1000 - 100
    assert poor_player.amount_chips.amount == initial_poor_chips + 10 + 100


def test_perform_panic():
    """Тест ивента паники"""
    casino = Casino()
    player = Player("Игрок", 100, Chip(50))
    goose = Goose("Паникер", 5)

    casino.register_player(player)
    casino.register_goose(goose)

    casino.perform_panic()

    assert player.balance == 0
    assert casino.balances[player.name] == 0

#
#
def test_perform_spin_win_defeat():
    """Тест ивента спин (выигрыш/слив)"""
    casino = Casino()
    player = Player("Игрок", 100, Chip(50))
    casino.register_player(player)

    initial_balance = player.balance
    initial_chips = player.amount_chips.amount

    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 2  # четное - выигрыш
        casino.perform_spin()

    assert player in casino.players
    assert player.balance == initial_balance * 2
    assert player.amount_chips.amount == initial_chips * 2

    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 3   # нечетное - проигрыш
        casino.perform_spin()

    assert player not in casino.players
    assert player.name not in casino.balances

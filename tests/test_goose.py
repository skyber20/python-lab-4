import pytest

from src.entities.player import Player
from src.entities.goose import Goose, HonkGoose, WarGoose


def test_goose_creation():
    """Тест создания обычного, боевого и орущего гусей"""
    goose = Goose("Гоша", 5)
    assert goose.name == "Гоша"
    assert goose.honk_volume == 5

    war_goose = WarGoose("Воин", 9)
    assert war_goose.name == "Воин"
    assert war_goose.honk_volume == 9
    assert isinstance(war_goose, Goose)

    honk_goose = HonkGoose("Крикун", 6)
    assert honk_goose.name == "Крикун"
    assert honk_goose.honk_volume == 6
    assert isinstance(honk_goose, Goose)


def test_goose_honk_volume_limits():
    """Тест ограничения громкости гуся"""
    # Нижний предел
    goose1 = Goose("Тихий", 0)
    assert goose1.honk_volume == 1

    # Верхний предел
    goose2 = Goose("Громкий", 15)
    assert goose2.honk_volume == 10


def test_goose_honk():
    """Тест крика гуся"""
    goose = Goose("Крикун", 8)
    honk_result = goose.honk()

    assert "Крикун" in honk_result
    assert "8" in honk_result
    assert "кричит" in honk_result


def test_war_goose_attack():
    """Тест атаки боевого гуся"""
    war_goose = WarGoose("Атакующий", 5)
    player = Player("Жертва", 100)

    initial_balance = player.balance
    result = war_goose.attack(player)

    assert player.balance < initial_balance
    assert "Атакующий" in result
    assert "Жертва" in result
    assert "атаковал" in result


def test_honk_goose_call():
    """Тест вызова орущего гуся"""
    honk_goose = HonkGoose("Че орешь", 4)
    player = Player("Чел", 100)

    initial_balance = player.balance
    result = honk_goose(player)

    assert player.balance != initial_balance
    assert "Че орешь" in result
    assert "Чел" in result
    assert 'слил' in result or 'залутал' in result


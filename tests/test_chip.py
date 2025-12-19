import pytest

from src.entities.chip import Chip

def test_chip_creation():
    """Тест создания фишки"""
    chip = Chip(100)
    assert chip.amount == 100

    with pytest.raises(ValueError):
        Chip(-50)


def test_chip_addition():
    """Тест сложения фишек"""
    chip1 = Chip(100)
    chip2 = Chip(50)
    result = chip1 + chip2

    assert isinstance(result, Chip)
    assert result.amount == 150

    with pytest.raises(TypeError):
        assert chip1 + 2

    with pytest.raises(ValueError):
        chip2 -= chip1


def test_chip_subtraction():
    """Тест вычитания фишек"""
    chip1 = Chip(100)
    chip2 = Chip(30)
    result = chip1 - chip2

    assert isinstance(result, Chip)
    assert result.amount == 70

    with pytest.raises(TypeError):
        assert chip1 - 2

    chip3 = Chip(50)
    # Так как amount получается отрицательным
    with pytest.raises(ValueError):
        assert chip3 - chip1


def test_chip_compare():
    """Тест оператора <"""
    chip1 = Chip(50)
    chip2 = Chip(100)

    assert chip1 < chip2
    assert chip1 < 100
    assert 40 < chip1

    assert chip2 > chip1
    assert 100 > chip1
    assert chip2 > 50

    assert chip1 <= chip2
    assert chip2 >= chip1

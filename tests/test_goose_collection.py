import pytest
from src._collections.goose_collection import GooseCollection
from src.entities.goose import Goose, WarGoose, HonkGoose
from src.exceptions import GooseNotFound


def test_goose_collection_creation():
    """Тест создания колллекции гусей"""
    gc = GooseCollection()
    assert len(gc) == 0
    assert list(gc) == []

    goose = Goose("Гоша", 5)
    gc.add(goose)

    assert len(gc) == 1
    assert gc[0] == goose

    geese = [
        Goose("Обычный", 3),
        WarGoose("Боевой", 8),
        HonkGoose("Орешник", 6)
    ]

    for goose in geese:
        gc.add(goose)

    assert len(gc) == 4
    for i in range(1, 4):
        assert gc[i] == geese[i-1]

    with pytest.raises(TypeError):
        gc.add("не гусь")


def test_remove_goose():
    """Тест удаления гуся"""
    gc = GooseCollection()
    goose1 = Goose("Гоша", 5)
    goose2 = WarGoose("Воин", 8)

    gc.add(goose1)
    gc.add(goose2)
    gc.remove_goose(goose1)

    assert len(gc) == 1
    assert goose2 in gc
    assert goose1 not in gc

    with pytest.raises(GooseNotFound):
        gc.remove_goose(goose1)


def test_remove_goose_by_name():
    """Тест удаления гуся по имени"""
    gc = GooseCollection()
    goose1 = Goose("Гоша", 5)
    goose2 = HonkGoose("Крикун", 7)

    gc.add(goose1)
    gc.add(goose2)
    gc.remove_goose_by_name("Гоша")

    assert len(gc) == 1
    assert gc[0] == goose2

    with pytest.raises(GooseNotFound):
        gc.remove_goose_by_name("Гоша")


def test_clear_geese():
    """Тест очистки коллекции"""
    gc = GooseCollection()
    gc.add(Goose("Гоша", 5))
    gc.add(WarGoose("Воин", 8))
    gc.add(HonkGoose("Крикун", 7))

    assert len(gc) == 3
    gc.clear_geese()
    assert len(gc) == 0


def test_get_names():
    """Тест получения списка имен"""
    gc = GooseCollection()
    gc.add(Goose("Гоша", 5))
    gc.add(WarGoose("Воин", 8))
    gc.add(HonkGoose("Крикун", 7))

    names = gc.get_names()
    assert names == ["Гоша", "Воин", "Крикун"]


def test_find_by_name():
    """Тест поиска гуся по имени"""
    gc = GooseCollection()
    goose1 = Goose("Гоша", 5)

    gc.add(goose1)

    found = gc.find_by_name("Гоша")
    assert found == goose1

    found = gc.find_by_name("Неизвестный")
    assert found is None


def test_filter_by_type():
    """Тест фильтрации по типу"""
    gc = GooseCollection()
    geese = [
        Goose("Обычный1", 3),
        Goose("Обычный2", 4),
        WarGoose("Боевой1", 8),
        WarGoose("Боевой2", 9),
        HonkGoose("Громкий1", 6),
        HonkGoose("Громкий2", 7)
    ]

    for goose in geese:
        gc.add(goose)

    # Фильтруем обычных гусей
    regular = gc.get_regular_geese()
    assert len(regular) == 2
    assert all(type(g) == Goose for g in regular)

    # Фильтруем боевых гусей
    war_geese = gc.filter_by_type(WarGoose)
    assert len(war_geese) == 2
    assert all(isinstance(g, WarGoose) for g in war_geese)

    # Фильтруем орущих гусей
    honk_geese = gc.filter_by_type(HonkGoose)
    assert len(honk_geese) == 2
    assert all(isinstance(g, HonkGoose) for g in honk_geese)


def test_get_regular_geese():
    """Тест получения только обычных гусей"""
    gc = GooseCollection()
    geese = [
        Goose("Обычный", 3),
        WarGoose("Боевой", 8),
        HonkGoose("Громкий", 6),
        Goose("Обычный2", 4)
    ]

    for goose in geese:
        gc.add(goose)

    regular = gc.get_regular_geese()
    assert all(g.name in ["Обычный", "Обычный2"] for g in regular)


def test_collection_addition():
    """Тест сложения коллекций через __add__"""
    gc1 = GooseCollection()
    gc2 = GooseCollection()

    goose1 = Goose("Гоша", 5)
    goose2 = WarGoose("Воин", 8)

    gc1.add(goose1)
    gc2.add(goose2)

    gc1 += gc2

    assert len(gc1) == 2
    assert goose1 in gc1 and goose2 in gc1

    with pytest.raises(TypeError):
        gc1 += "не гусь"


def test_collection_slice():
    """Тест среза коллекции"""
    gc = GooseCollection()
    geese = [Goose(f"Гусь{i}", i + 1) for i in range(5)]

    for goose in geese:
        gc.add(goose)

    sliced = gc[1:4]
    assert len(sliced) == 3
    assert sliced[0] == geese[1]
    assert sliced[1] == geese[2]
    assert sliced[2] == geese[3]

    sliced_step = gc[0:5:2]
    assert len(sliced_step) == 3
    assert sliced_step[0] == geese[0]
    assert sliced_step[1] == geese[2]
    assert sliced_step[2] == geese[4]

    gc.clear_geese()
    sliced = gc[1:4]
    assert len(sliced) == 0


def test_collection_index_error():
    """Тест выхода за границы индекса"""
    gc = GooseCollection()
    goose = Goose("Гоша", 5)
    gc.add(goose)

    assert gc[-1] == goose

    with pytest.raises(IndexError):
        index = gc[10]


def test_collection_iteration():
    """Тест итерации по коллекции"""
    gc = GooseCollection()
    geese = [Goose(f"Гусь{i}", i + 1) for i in range(3)]

    for goose in geese:
        gc.add(goose)

    for i, goose in enumerate(gc):
        assert goose == geese[i]


def test_collection_contains():
    """Тест оператора in"""
    gc = GooseCollection()
    goose1 = Goose("Гоша", 5)
    goose2 = WarGoose("Воин", 8)

    gc.add(goose1)

    assert goose1 in gc
    assert goose2 not in gc

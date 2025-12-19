from typing import Any
from src.entities.goose import Goose, HonkGoose, WarGoose
from src.exceptions import GooseNotFound


class GooseCollection:
    def __init__(self):
        """Колекция гусей"""
        self._geese = []

    def __add__(self, other):
        new_collection = GooseCollection()
        new_collection._geese = self._geese.copy()

        if isinstance(other, (Goose, HonkGoose, WarGoose)):
            new_collection._geese.append(other)
        elif isinstance(other, GooseCollection):
            new_collection._geese.extend(other._geese)
        else:
            raise TypeError(f"Нельзя добавить {type(other)} к GooseCollection")

        return new_collection

    def __len__(self):
        return len(self._geese)

    def __iter__(self):
        return iter(self._geese)

    def __getitem__(self, ind):
        if isinstance(ind, slice):
            start, stop, step = ind.indices(len(self._geese))
            new_collection = GooseCollection()
            new_collection._geese= self._geese[start:stop:step]
            return new_collection

        try:
            return self._geese[ind]
        except IndexError:
            raise IndexError("Индекс вышел за границы коллекции гусей")

    def __contains__(self, goose):
        return goose in self._geese

    def __repr__(self):
        return f"GooseCollection(geese={self._geese})"

    def add(self, other: Any) -> None:
        """
        Прибавить гуся или коллекцию гусей к существующей
        :param other: Гусь или другая коллекция гусей
        :return:
        """
        if isinstance(other, (Goose, HonkGoose, WarGoose)):
            self._geese.append(other)
        elif isinstance(other, GooseCollection):
            self._geese.extend(other._geese)
        else:
            raise TypeError(f"Нельзя добавить {type(other)} к GooseCollection")

    def remove_goose(self, goose: Goose) -> None:
        """
        Удаляет гуся
        :param goose: гусь
        :return:
        """
        if goose not in self._geese:
            raise GooseNotFound(goose)
        self._geese.remove(goose)

    def remove_goose_by_name(self, goose_name: str) -> None:
        """
        Удаляет гуся по имени
        :param goose_name: Имя гуся
        :return:
        """
        for goose in self._geese:
            if goose.name == goose_name:
                self._geese.remove(goose)
                return
        raise GooseNotFound(goose_name)

    def clear_geese(self) -> None:
        """Очистить коллекцию гусей"""
        self._geese.clear()

    def get_names(self) -> list[str]:
        """Имена всех гусей"""
        return [g.name for g in self._geese]

    def find_by_name(self, goose_name: str) -> Goose | None:
        """
        Найти гуся по имени
        :param goose_name: имя гуся
        :return: гусь
        """
        for goose in self._geese:
            if goose.name == goose_name:
                return goose
        return None

    def filter_by_type(self, goose_type) -> list[Goose]:
        """
        Отфильтровать по типу Гуся (если Goose, то вернет всех гусей в коллекции)
        :param goose_type: тип гуся
        :return: Гуси типа goose_type
        """
        return [g for g in self._geese if isinstance(g, goose_type)]

    def get_regular_geese(self) -> list[Goose]:
        """Только дэфолтные гуси"""
        return [g for g in self._geese if type(g) == Goose]

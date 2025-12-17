from src.entities.goose import Goose, HonkGoose, WarGoose
from src.exceptions import GooseNotFound


class GooseCollection:
    def __init__(self):
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

    def add(self, other):
        if isinstance(other, (Goose, HonkGoose, WarGoose)):
            self._geese.append(other)
        elif isinstance(other, GooseCollection):
            self._geese.extend(other._geese)
        else:
            raise TypeError(f"Нельзя добавить {type(other)} к GooseCollection")

    def remove_goose(self, goose):
        if goose not in self._geese:
            raise GooseNotFound(goose)
        self._geese.remove(goose)

    def remove_goose_by_name(self, goose_name: str):
        for goose in self._geese:
            if goose.name == goose_name:
                self._geese.remove(goose)
                return
        raise GooseNotFound(goose_name)

    def clear_geese(self):
        self._geese.clear()

    def get_names(self):
        return [g.name for g in self._geese]

    def find_by_name(self, goose_name: str):
        for goose in self._geese:
            if goose.name == goose_name:
                return goose
        return None

    def filter_by_type(self, goose_type):
        return [g for g in self._geese if isinstance(g, goose_type)]

    def get_regular_geese(self):
        return [g for g in self._geese if type(g) == Goose]

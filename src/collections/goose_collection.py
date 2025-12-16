from src.entities.goose import Goose, HonkGoose, WarGoose
from src.exceptions import GooseNotFound


class GooseCollection:
    def __init__(self):
        self._geese = []

    def __add__(self, goose):
        if not isinstance(goose, (Goose, HonkGoose, WarGoose)):
            raise TypeError('В коллекцию гусей можео добавлять только Goose, HonkGoose, WarGoose')
        self._geese.append(goose)

    def __remove__(self, goose):
        if goose not in self._geese:
            raise GooseNotFound(goose.name)
        self._geese.remove(goose)

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
            raise IndexError("Индекс вышел за границы коллекции игроков")

    def __repr__(self):
        return f"GooseCollection(players={self._geese})"
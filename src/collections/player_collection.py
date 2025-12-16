from src.entities.player import Player
from src.exceptions import PlayerNotFound


class PlayerCollection:
    def __init__(self):
        self._players = []

    def __add__(self, player: Player):
        if not isinstance(player, Player):
            raise TypeError('В коллекцию игроков можео добавлять только Player')
        self._players.append(player)

    def __remove__(self, player: Player):
        if player not in self._players:
            raise PlayerNotFound(player.name)
        self._players.remove(player)

    def __len__(self):
        return len(self._players)

    def __iter__(self):
        return iter(self._players)

    def __getitem__(self, ind):
        if isinstance(ind, slice):
            start, stop, step = ind.indices(len(self._players))
            new_collection = PlayerCollection()
            new_collection._players = self._players[start:stop:step]
            return new_collection

        try:
            return self._players[ind]
        except IndexError:
            raise IndexError("Индекс вышел за границы коллекции игроков")

    def __repr__(self):
        return f"PlayerCollection(players={self._players})"
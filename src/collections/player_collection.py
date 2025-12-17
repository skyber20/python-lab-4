from src.entities.player import Player
from src.exceptions import PlayerNotFound


class PlayerCollection:
    def __init__(self):
        self._players = []

    def __add__(self, other):
        new_collection = PlayerCollection()
        new_collection._players = self._players.copy()

        if isinstance(other, Player):
            new_collection._players.append(other)
        elif isinstance(other, PlayerCollection):
            new_collection._players.extend(other._players)
        else:
            raise TypeError(f"Нельзя добавить {type(other)} к PlayerCollection")

        return new_collection

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

    def __contains__(self, player: Player):
        return player in self._players

    def __repr__(self):
        return f"PlayerCollection(players={self._players})"

    def add(self, other):
        if isinstance(other, Player):
            self._players.append(other)
        elif isinstance(other, PlayerCollection):
            self._players.extend(other._players)
        else:
            raise TypeError(f"Нельзя добавить {type(other)} к PlayerCollection")


    def remove_player(self, player: Player):
        if player not in self._players:
            raise PlayerNotFound(player)
        self._players.remove(player)

    def remove_player_by_name(self, player_name: str):
        for player in self._players:
            if player.name == player_name:
                self._players.remove(player)
                return
        raise PlayerNotFound(player_name)

    def clear_players(self):
        self._players.clear()

    def get_names(self):
        return [p.name for p in self._players]

    def find_by_name(self, player_name: str):
        for player in self._players:
            if player.name == player_name:
                return player
        return None

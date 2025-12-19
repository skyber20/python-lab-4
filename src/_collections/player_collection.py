from typing import Any
from src.entities.player import Player
from src.exceptions import PlayerNotFound


class PlayerCollection:
    def __init__(self):
        """Коллеция игроков"""
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

    def __contains__(self, player):
        return player in self._players

    def __repr__(self):
        return f"PlayerCollection(players={self._players})"

    def add(self, other: Any) -> None:
        """
        Добавить нового игрока или коллекцию игроков
        :param other: Игрок или Коллеция игроков
        :return: ничего
        """
        if isinstance(other, Player):
            self._players.append(other)
        elif isinstance(other, PlayerCollection):
            self._players.extend(other._players)
        else:
            raise TypeError(f"Нельзя добавить {type(other)} к PlayerCollection")


    def remove_player(self, player: Player) -> None:
        """
        Удаляет игрока из коллекции
        :param player: игрок
        :return: ничего
        """
        if player not in self._players:
            raise PlayerNotFound(player)
        self._players.remove(player)

    def remove_player_by_name(self, player_name: str) -> None:
        """
        Удаляет игрока по имени
        :param player_name: имя игрока
        :return:
        """
        for player in self._players:
            if player.name == player_name:
                self._players.remove(player)
                return
        raise PlayerNotFound(player_name)

    def clear_players(self) -> None:
        """Очистить всю коллекцию игроков"""
        self._players.clear()

    def get_names(self) -> list[str]:
        """Все имена игроков в коллекции"""
        return [p.name for p in self._players]

    def find_by_name(self, player_name: str) -> Player | None:
        """
        Найти игрока по имени
        :param player_name: имя игрока
        :return: игрок
        """
        for player in self._players:
            if player.name == player_name:
                return player
        return None

    def rich_player(self) -> Player | None:
        """Найти богатого игрока (количество фишек + баланс)"""
        mx = -10000000
        p = None
        for player in self._players:
            if player.amount_chips.amount + player.balance > mx:
                mx = player.amount_chips.amount + player.balance
                p = player
        return p

    def poor_player(self) -> Player | None:
        """Найти бедного игрока (количество фишек + баланс)"""
        mn = 1000000000000
        p = None
        for player in self._players:
            if player.amount_chips.amount + player.balance < mn:
                mn = player.amount_chips.amount + player.balance
                p = player
        return p

from src.collections.player_collection import PlayerCollection
from src.entities.player import Player
from src.exceptions import PlayerNotFound
from src.my_logger import logger


class CasinoBalance:
    def __init__(self):
        self._balances = {}

    def __setitem__(self, player_name: str, balance: int):
        old_balance = self._balances.get(player_name, 'не было')
        self._balances[player_name] = balance
        if old_balance != 'не было':
            logger.info(f"Баланс игрока {player_name} изменен: {old_balance} -> {balance}")

    def __delitem__(self, player_name: str):
        try:
            del self._balances[player_name]
            logger.info(f'Как жаль, игрок {player_name} обанкротился и он выходит из игры')
        except KeyError:
            raise PlayerNotFound(player_name)

    def __getitem__(self, player_name: str):
        if not player_name in self._balances:
            raise PlayerNotFound(player_name)

        return self._balances[player_name]

    def __contains__(self, player_name: str):
        return player_name in self._balances

    def __iter__(self):
        return iter(self._balances)

    def __len__(self):
        return len(self._balances)

    def __repr__(self):
        return f"CasinoBalance()"

    def add_player(self, player: Player):
        self._balances[player.name] = player.balance

    def push_players(self, players: PlayerCollection):
        for player in players:
            self._balances[player.name] = player.balance
